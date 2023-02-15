import _ from 'lodash'
import Vue from 'vue'
import {addToSearchHistory, getMySearchHistory} from '@/api/search'
import {getAllTopics} from '@/api/topics'

const state = {
  author: null,
  domain: undefined,
  fromDate: null,
  includeAdmits: undefined,
  includeCourses: undefined,
  includeNotes: undefined,
  includeStudents: undefined,
  isFocusOnSearch: false,
  postedBy: 'anyone',
  queryText: undefined,
  searchHistory: [],
  showAdvancedSearch: false,
  student: null,
  toDate: null,
  topic: null,
  topicOptions: []
}

const getters = {
  author: (state: any): string => state.author,
  domain: (state: any): string[] => state.domain,
  fromDate: (state: any): string => state.fromDate,
  includeAdmits: (state: any): boolean => state.includeAdmits,
  includeCourses: (state: any): boolean => state.includeCourses,
  includeNotes: (state: any): boolean => state.includeNotes,
  includeStudents: (state: any): boolean => state.includeStudents,
  isFocusOnSearch: (state: any): boolean => state.isFocusOnSearch,
  postedBy: (state: any): string => state.postedBy,
  queryText: (state: any): string => state.queryText,
  showAdvancedSearch: (state: any): boolean => state.showAdvancedSearch,
  student: (state: any): string => state.student,
  toDate: (state: any): string => state.toDate,
  topic: (state: any): string => state.topic,
  topicOptions: (state: any): string[] => state.topicOptions
}

const mutations = {
  resetAdvancedSearch: (state: any, queryText?: string) => {
    const currentUser = Vue.prototype.$currentUser
    const domain = ['students']
    if (currentUser.canAccessCanvasData) {
      domain.push('courses')
    }
    if (currentUser.canAccessAdvisingData) {
      domain.push('notes')
    }
    if (currentUser.canAccessAdmittedStudents) {
      domain.push('admits')
    }
    state.domain = domain
    state.author = null
    state.fromDate = null
    state.postedBy = 'anyone'
    state.student = null
    state.queryText = queryText
    state.toDate = null
    state.topic = null
    state.includeAdmits = domain.includes('admits')
    state.includeCourses = domain.includes('courses')
    state.includeNotes = domain.includes('notes')
    state.includeStudents = domain.includes('students')
  },
  setDomain: (state: any, domain: string) => state.domain = domain,
  setAuthor: (state: any, value: string) => state.author = value,
  setFromDate: (state: any, value: string) => state.fromDate = value,
  setPostedBy: (state: any, value: string) => state.postedBy = value,
  setStudent: (state: any, value: string) => state.student = value,
  setToDate: (state: any, value: string) => state.toDate = value,
  setTopic: (state: any, value: string) => state.topic = value,
  setIncludeAdmits: (state: any, value: boolean) => state.includeAdmits = value,
  setIncludeCourses: (state: any, value: boolean) => state.includeCourses = value,
  setIncludeNotes: (state: any, value: boolean) => state.includeNotes = value,
  setIncludeStudents: (state: any, value: boolean) => state.includeStudents = value,
  setIsFocusOnSearch: (state: any, value: boolean) => state.isFocusOnSearch = value,
  setSearchHistory: (state: any, searchHistory: any[]) => state.searchHistory = searchHistory,
  setShowAdvancedSearch: (state: any, show: boolean) => state.showAdvancedSearch = show,
  setTopicOptions: (state: any, topicOptions: any[]) => state.topicOptions = topicOptions,
  setQueryText: (state: any, queryText: string) => state.queryText = queryText
}

const actions = {
  init: ({commit}, queryText?: string) => {
    return new Promise<void>(resolve => {
      commit('resetAdvancedSearch', queryText)

      getAllTopics(true).then(rows => {
        const topicOptions: any[] = []
        _.each(rows, row => {
          const topic = row['topic']
          topicOptions.push({
            text: topic,
            value: topic
          })
        })
        commit('setTopicOptions', topicOptions)
        getMySearchHistory().then(history => {
          commit('setSearchHistory', history)
          return resolve()
        })
      })
    })
  },
  resetAdvancedSearch: ({commit}) => commit('resetAdvancedSearch'),
  setAuthor: ({commit}, value: string) => commit('setAuthor', value),
  setFromDate: ({commit}, value: string) => commit('setFromDate', value),
  setIsFocusOnSearch: ({commit}, value: boolean) => commit('setIsFocusOnSearch', value),
  updateSearchHistory: ({commit}, query: string) => {
    query = _.trim(query)
    if (query) {
      addToSearchHistory(query).then(history => commit('setSearchHistory', history))
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}