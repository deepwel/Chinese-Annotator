import Vue from 'vue'
import Router from 'vue-router'

import LoadingPage from '@/components/LoadingPage'
import WorkingSpace from '@/components/WorkingSpace'
import TextClassification from '@/components/workspaces/TextClassification'

const router = new Router({
	routes : [
		{path : '/loading', component : LoadingPage},
		{path : '/working-space' , component : WorkingSpace, children : [
			{path : 'text-classify', component : TextClassification}
		]},

	]
})
export default router
