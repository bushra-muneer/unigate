import { useApiFetch } from '#imports';

interface FeedbackPayload {
  student_id: string;
  group_id: string;
  question_id: string;
  answer: string;
  exam_date: string;
}

interface HelpfulnessStat {
  group_size: string;
  helpful_pct: number;
  not_helpful_pct: number;
  not_answered_pct: number;
}

export function useFeedback() {
  const saveAnswer = async (payload: FeedbackPayload) => {
    try {
      await useApiFetch('/unigate/feedback/response', {
        method: 'POST',
        body: payload,
      });
    } catch (e) {
      console.error('Failed to save answer inside useFeedback:', e);
      throw e;
    }
  };

  const getHelpfulnessStats = async (examDate: string | null = null): Promise<HelpfulnessStat[]> => {
    try {
      const queryParam = examDate ? `?exam_date=${examDate}` : '';
      const response = await useApiFetch(`/feedback/helpfulness-distribution${queryParam}`, {
        method: 'GET',
      });
      return response as HelpfulnessStat[];
    } catch (error) {
      console.error('Failed to fetch helpfulness stats:', error);
      return [];
    }
  };

  return {
    saveAnswer,
    getHelpfulnessStats,
  };
}
