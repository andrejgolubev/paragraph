import { useUiStore } from "../store/uiStore"

export const BASE_URL = "https://192.168.0.108:8000"

export const headers = { "Content-Type": "application/json"}


export const fetchUrl = async (url, options = {}) => {
  try {
    return await fetch(url, { credentials: "include", ...options })
  } catch (err) {
    if (err.message === 'Failed to fetch') {
      const message = "Ошибка сети :("
      showNotification(message, "error")
      throw { type: "network_error", detail: message }
    }
  }
}

export const getHandledResponseData = async (response) => {
  if (response.status === 429) {
    const body = await response.json().catch(() => ({}))
    const errorDetail = body.detail
    showNotification(errorDetail, "error")
  }
  if (!response.ok && response.status !== 401) {
    const body = await response.json().catch(() => ({}))
    const errorDetail = body.detail
    showNotification(errorDetail, "error")
  }

  return await response.json()
}


async function apiFetch(url, options = {}) {
    const response = await fetchUrl(url, options)
    
    const responseData = await getHandledResponseData(response)
  
    return responseData
}


export function showNotification(message, type = "error") {
  const { 
    setNotificationOuterMessage, 
    setNotificationOuterActive, 
    setNotificationOuterType, 
  } = useUiStore.getState()

  console.log('showNotification called')

  setNotificationOuterType(type)
  setNotificationOuterMessage(message)
  setNotificationOuterActive(true)

}

const API = {
  getScheduleData: async ({ groupDataValue, dateDataValue }) => {
    const url =
      `${BASE_URL}/schedule/get-schedule?group_data_value=${groupDataValue}` +
      (dateDataValue ? `&date_data_value=${dateDataValue}` : "")
    return apiFetch(url)
  },

  saveHomework: async (
    groupDataValue,
    dateDataValue,
    lessonIndex,
    homeworkText
  ) => {
    const payload = {
      group_data_value: String(groupDataValue),
      date_data_value: String(dateDataValue),
      lesson_index: Number(lessonIndex),
      homework: String(homeworkText),
    }

    return apiFetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    })
  },

  loadHomeworkData: async (groupDataValue, dateDataValue, lessonIndex) => {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
      lesson_index: parseInt(lessonIndex),
    })

    return apiFetch(`${BASE_URL}/homework/get?${params.toString()}`, {
      method: "GET",
    })
  },

  loadGroups: async () => {
    return apiFetch(`${BASE_URL}/schedule/get-all-groups`, {
      method: "GET",
    })
  },

  loadDates: async () => {
    return apiFetch(`${BASE_URL}/schedule/get-all-dates`, {
      method: "GET",
    })
  },

  convertToDataValue: async ({ groupNumber = "", date = "" }) => {
    const params = new URLSearchParams({
      group_number: String(groupNumber),
      date: date,
    })

    return apiFetch(`${BASE_URL}/homework/convert?${params.toString()}`, {
      method: "GET",
    })
  },

  convertFromDataValue: async ({ groupDataValue, dateDataValue }) => {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue ?? "",
    })

    return apiFetch(`${BASE_URL}/homework/convert-back?${params.toString()}`, {
      method: "GET",
    })
  },

  getAllGroups: async () => {
    return apiFetch(`${BASE_URL}/schedule/get-all-groups`, { method: "GET" })
  },

  getUserData: async () => {
    return apiFetch(`${BASE_URL}/user/me`, 
      { method: "GET", headers }
    )
  },

  logout: async () => {
    return apiFetch(
      `${BASE_URL}/user/logout`, 
      { method: "POST", headers }
    )
  },

  updateUserData: async ({ email, password, username, group }) => {
    return apiFetch(
      `${BASE_URL}/user/update-profile`, {
        method: "PATCH",
        headers,
        body: JSON.stringify({ email, password, username, group_number: group }),
      })
  },
}

export default API