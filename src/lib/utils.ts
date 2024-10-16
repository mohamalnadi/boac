import _ from 'lodash'
import {nextTick} from 'vue'

export function oxfordJoin(arr, zeroString) {
  switch((arr || []).length) {
    case 0: return _.isNil(zeroString) ? '' : zeroString
    case 1: return _.head(arr)
    case 2: return `${_.head(arr)} and ${_.last(arr)}`
    default: return _.join(_.concat(_.initial(arr), `and ${_.last(arr)}`), ', ')
  }
}

export function putFocusNextTick(id: string, cssSelector?: string) {
  nextTick(() => {
    let counter = 0
    const putFocus = setInterval(() => {
      let el = document.getElementById(id)
      el = el && cssSelector ? el.querySelector(cssSelector) : el
      el && el.focus()
      if (el || ++counter > 5) {
        // Abort after success or three attempts
        clearInterval(putFocus)
      }
    }, 500)
  })
}

export function sortComparator(a, b, nullFirst=true) {
  if (_.isNil(a) || _.isNil(b)) {
    if (nullFirst) {
      return _.isNil(a) ? (_.isNil(b) ? 0 : -1) : 1
    } else {
      return _.isNil(b) ? (_.isNil(a) ? 0 : -1) : 1
    }
  } else if (_.isNumber(a) && _.isNumber(b)) {
    return a < b ? -1 : a > b ? 1 : 0
  } else {
    const aInt = toInt(a)
    const bInt = toInt(b)
    if (aInt && bInt) {
      return aInt < bInt ? -1 : aInt > bInt ? 1 : 0
    } else {
      return a.toString().localeCompare(b.toString(), undefined, {
        numeric: true
      })
    }
  }
}

export function stripHtmlAndTrim(html) {
  let text = html && html.replace(/<([^>]+)>/ig,'')
  text = text && text.replace(/&nbsp;/g, '')
  return _.trim(text)
}

export function toInt(value, defaultValue = null) {
  const parsed = parseInt(value, 10)
  return Number.isInteger(parsed) ? parsed : defaultValue
}
