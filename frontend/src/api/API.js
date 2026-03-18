import { useUiStore } from "../store/uiStore"


const BASE_URL =
    APP__LOCAL_STACK === 'true'
    ? "/api"
    : APP__DEV === "true" 
    ? "https://localhost:8000" 
    : APP__API_HOST

    
const headers = { "Content-Type": "application/json"}


const fetchUrl = async (url, options = {}) => {
  try {
    return await fetch(url, { credentials: "include", ...options })
  } catch (err) {
    if (err.message === 'Failed to fetch') {
      const message = "Ошибка сети :("
      showNotificationOuter(message, "error")
      throw { type: "network_error", detail: message }
    }
  }
}

const getHandledResponseData = async (response) => {
  const body = await response.json().catch(() => ({}))
  if (response.status > 403) {
    showNotificationOuter(body.detail, "error")
  }
  return body
}


async function apiFetch(url, options = {}) {
  const response = await fetchUrl(url, options)
  const responseData = await getHandledResponseData(response)
  return responseData
}


export function showNotificationOuter(message, type, fromLeft=false) {
  const { 
    setNotificationOuterMessage, 
    setNotificationOuterActive, 
    setNotificationOuterType, 
    setNotificationOuterIsLeft, 
  } = useUiStore.getState()

  setNotificationOuterMessage(message)
  setNotificationOuterType(type)
  setNotificationOuterIsLeft(fromLeft)
  setTimeout( async () => {
    setNotificationOuterActive(true)
  }, 50) 
}

class NotesAPI {
  saveNote = async (
    userId,
    lessonIndex,
    homeworkText
  ) => {
    const payload = {
      user_id: String(userId),
      lesson_index: Number(lessonIndex),
      homework: String(homeworkText),
    }

    return apiFetch(`${BASE_URL}/notes/save`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    }, )
  }
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
    }, )
  },

  getHomework: async (groupDataValue, dateDataValue, lessonIndex) => {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
      lesson_index: parseInt(lessonIndex),
    })

    return apiFetch(`${BASE_URL}/homework/get?${params.toString()}`, {
      method: "GET",
    })
  },

  notes: new NotesAPI(),

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

  sendRegisterData: async (
    email,
    password,
    username,
    group,
    acceptPd,
    acceptTerms
  ) => {
    return apiFetch(
      `${BASE_URL}/user/register`,
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          username,
          email,
          password,
          group_number: group,
          accept_pd: acceptPd,
          accept_terms: acceptTerms,
        }),
      },
    )
  },

  sendLoginData: async (email, password) => {
    const url = `${BASE_URL}/user/login`
    return apiFetch(
      url,
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          email,
          password,
        }),
      },
    )
  },

  logout: async () => {
    return apiFetch(
      `${BASE_URL}/user/logout`, 
      { method: "POST", headers }, 
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

  getHomeworksMap: async (groupDataValue, dateDataValue) => {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue ?? "",
    })
    return apiFetch(
      `${BASE_URL}/homework/get-all?${params.toString()}`, {
        method: "GET",
        headers,
      }
    )
  }
}

export default API