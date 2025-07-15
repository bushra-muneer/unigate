import { useApiFetch } from '#imports';

// Определяем интерфейс для данных с правильными именами полей
interface FeedbackPayload {
  student_id: string;
  group_id: string;
  question_id: string;
  answer: string;
  exam_date: string;
}

export function useFeedback() {
  // Функция принимает один объект payload, чтобы избежать путаницы с именами
  const saveAnswer = async (payload: FeedbackPayload) => {
    // Эта функция просто берет ГОТОВЫЙ объект payload и отправляет его целиком.
    // Она больше не пытается его пересобирать.
    try {
      await useApiFetch('/unigate/feedback/response', {
        method: 'POST',
        body: payload, // Отправляем весь объект целиком
      });
    } catch (e) {
      console.error('Failed to save answer inside useFeedback:', e);
      // Пробрасываем ошибку дальше, чтобы ее можно было обработать в компоненте, если нужно
      throw e;
    }
  };

  return { saveAnswer };
}