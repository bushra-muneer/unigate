import { ref } from "vue";

export function useGroups() {
  const groups = useState("groups", () => ref([]));
  const isLoading = ref(false);
  const isError = ref(false);
  const { currentStudent, getCurrentStudent } = useCurrentStudent();

  // Ensure user is authenticated before making requests
  const ensureAuthenticated = async () => {
    if (!currentStudent.value) {
      await getCurrentStudent();
    }
    if (!currentStudent.value) {
      throw new Error("User not authenticated");
    }
    return currentStudent.value;
  };

  // Add this function to check authentication status
  const checkAuthStatus = async () => {
    try {
      if (!currentStudent.value) {
        await getCurrentStudent();
      }
      return !!currentStudent.value;
    } catch (error) {
      return false;
    }
  };

  async function getAllGroups() {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/groups", {
        method: "GET",
      });
      groups.value = response;
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupCount(courseName: string) {
    try {
      // await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/courses/get_group_number?course_name=${encodeURIComponent(courseName)}`,
        {
          method: "GET",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getAverageMembers(courseName: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/courses/${encodeURIComponent(courseName)}/average_members`,
        { method: "GET" },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getActiveGroupCount(courseName: string, examDate: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const queryParams = new URLSearchParams({
        exam_date: examDate,
      }).toString();
      const url = `/courses/${encodeURIComponent(courseName)}/active?${queryParams}`;
      const response = await useApiFetch(url, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupCreationDistribution(courseName: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/courses/${encodeURIComponent(courseName)}/distribution`,
        {
          method: "GET",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function searchGroups(queryParams: Record<string, any> = {}) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;

      const queryString = new URLSearchParams(
        Object.entries(queryParams).reduce(
          (acc, [key, value]) => {
            if (value !== undefined) acc[key] = value.toString();
            return acc;
          },
          {} as Record<string, string>,
        ),
      ).toString();

      const response = await useApiFetch(`/groups/search?${queryString}`, {
        method: "GET",
      });

      groups.value = response;

      return response; // Added return statement
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupById(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function createGroup(groupData: any) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/groups", {
        method: "POST",
        body: groupData,
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function joinGroup(groupId: string) {
    try {
      await getCurrentStudent();

      if (!currentStudent.value) {
        throw new Error("No student found");
      }

      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/join`, {
        method: "POST",
        body: {
          student_id: currentStudent.value.id,
        },
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function leaveGroup(groupId: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/leave`, {
        method: "POST",
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupStudents(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/students`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupRequests(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/requests`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function handleGroupRequest(
    groupId: string,
    requestId: string,
    action: "approve" | "reject" | "block",
  ) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/groups/${groupId}/requests/${requestId}/${action}`,
        {
          method: "POST",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function handleUserBlock(
    groupId: string,
    studentId: string,
    action: "block" | "unblock",
  ) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/groups/${groupId}/students/${studentId}/${action}`,
        {
          method: "POST",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  //Function to fetch courses
  async function getCourses() {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/courses", {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  //Function to fetch professors courses
  async function getProfessorsCourses() {
    try {
      // await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/unigate/professors/courses", {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  // Function to fetch professor's courses with group details
async function getCoursesWithGroups() {
  try {
    isError.value = false;
    isLoading.value = true;
    const response = await useApiFetch("/unigate/professors/courses-with-groups", {
  method: "GET",
});
    return response;
  } catch (error) {
    isError.value = true;
    throw error;
  } finally {
    isLoading.value = false;
  }
}


  async function getYearlyStats(courseName: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/courses/${encodeURIComponent(courseName)}/yearly_stats`,
        {
          method: "GET",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupMemberCount(groupId: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/students`);
      if (!response || typeof response !== 'object') return 0;

      const students = Array.isArray((response as any).students) ? (response as any).students : [];
      const superStudents = Array.isArray((response as any).super_students) ? (response as any).super_students : [];

      const uniqueIds = new Set<string>();
      for (const s of students) uniqueIds.add(s.id);
      for (const s of superStudents) uniqueIds.add(s.id);

      return uniqueIds.size;
    } catch (error) {
      isError.value = true;
      console.error('Failed to fetch member count:', error);
      return 0;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    groups,
    isLoading,
    isError,
    currentStudent,
    getAllGroups,
    getGroupById,
    createGroup,
    joinGroup,
    leaveGroup,
    getGroupStudents,
    getGroupRequests,
    handleGroupRequest,
    handleUserBlock,
    checkAuthStatus,
    getCourses,
    searchGroups,
    getGroupCount,
    getProfessorsCourses,
    getAverageMembers,
    getActiveGroupCount,
    getGroupCreationDistribution,
    getYearlyStats, 
    getCoursesWithGroups,
    getGroupMemberCount,
  };
}
