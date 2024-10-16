import 'vuetify/styles'
import {aliases, mdi} from 'vuetify/iconsets/mdi-svg'
import {createVuetify} from 'vuetify'
import {VAppBar, VAppBarTitle} from 'vuetify/components/VAppBar'
import {VApp} from 'vuetify/components/VApp'
import {VBtn} from 'vuetify/components/VBtn'
import {VIcon} from 'vuetify/components/VIcon'
import {VImg} from 'vuetify/components/VImg'
import {VList, VListItem, VListItemAction, VListItemSubtitle, VListItemTitle} from 'vuetify/components/VList'
import {VMain} from 'vuetify/components/VMain'
import {VMenu} from 'vuetify/components/VMenu'
import {VProgressCircular} from 'vuetify/components/VProgressCircular'
import {VTextarea} from 'vuetify/components/VTextarea'
import {VTextField} from 'vuetify/components/VTextField'

// @ts-ignore
import colors from 'vuetify/lib/util/colors'

export default createVuetify({
  components: {
    VApp,
    VAppBar,
    VAppBarTitle,
    VBtn,
    VIcon,
    VImg,
    VList,
    VListItem,
    VListItemAction,
    VListItemSubtitle,
    VListItemTitle,
    VMain,
    VMenu,
    VProgressCircular,
    VTextarea,
    VTextField
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  },
  theme: {
    themes: {
      light: {
        colors: {
          alert: '#fef6e6',
          error: '#b94a48',
          info: '#367DA1',
          primary: '#377695',
          red: colors.red.darken1,
          secondary: '#eee',
          success: '#437F4B'
        }
      }
    }
  }
})
