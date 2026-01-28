import { useUiStore } from "../store/uiStore"

const BASE_URL =
    __VITE_DEV__  === "true"
    ? "https://192.168.0.108:8000"
    : __VITE_API_HOST__

    
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


async function authApiFetch(url, options = {}, additional = {}) {
  const response = await fetchUrl(url, options)
  const responseData = await getHandledResponseData(response)
  return { ...responseData, ...additional }
}


export function showNotificationOuter(message, type) {
  const { 
    setNotificationOuterMessage, 
    setNotificationOuterActive, 
    setNotificationOuterType, 
  } = useUiStore.getState()

  setNotificationOuterMessage(message)
  setNotificationOuterType(type)
  setTimeout( async () => {
    setNotificationOuterActive(true)
  }, 50) 
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

  sendRegisterData: async (
    email,
    password,
    username,
    group,
    acceptPd,
    acceptTerms
  ) => {
    return authApiFetch(
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
      {
        type: "sign-up",
      }
    )
  },

  sendLoginData: async (email, password) => {
    const url = `${BASE_URL}/user/login`
    return authApiFetch(
      url,
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          email,
          password,
        }),
      },
      { type: "sign-in" }
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
}

export default API