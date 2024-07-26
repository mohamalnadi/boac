import axios from 'axios'
import {useContextStore} from '@/stores/context'
import utils from '@/api/api-utils'

export function ping() {
  return axios
    .get(`${utils.apiBaseUrl()}/api/ping`)
    .then(response => response.data, () => null)
}

export function getVersion() {
  return axios
    .get(`${utils.apiBaseUrl()}/api/version`)
    .then(response => response)
}

export function getServiceAnnouncement() {
  return axios
    .get(`${utils.apiBaseUrl()}/api/service_announcement`)
    .then(response => response)
}

export function publishAnnouncement(publish) {
  return axios
    .post(`${utils.apiBaseUrl()}/api/service_announcement/publish`, {publish: publish})
    .then(response => {
      const data = response
      useContextStore().setServiceAnnouncement(data)
      return data
    })
    .catch(error => error)
}

export function updateAnnouncement(text) {
  return axios
    .post(`${utils.apiBaseUrl()}/api/service_announcement/update`, {text: text})
    .then(response => {
      const data = response
      useContextStore().setServiceAnnouncement(data)
      return data
    })
    .catch(error => error)
}
