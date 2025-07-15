import { useApiFetch } from "@/composables/useApiFetch";

export async function fetchCurrentStudent() {
  return await useApiFetch("/unigate/students/me", {
    method: "GET",
  });
}
