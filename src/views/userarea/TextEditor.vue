<template>
    <!-- Wrap in Suspense for loading SyncFusion and Loading Data! -->
    <div class="text-white border-white m-2 border-y-2 justify-center flex">
        <RouterLink to="/account">Back to Account</RouterLink>
    </div>
    <div class="text-white">
        <div id="story dropdown" v-if="navigationStore.storyDropDown.stories.showStoryDropdown">
            Something
            <DropDown :stories="navigationStore.storyDropDown.stories"></DropDown>
        </div>
        <div>
            --- Button (conditional -> No Story exists yet): Create new Story ---
        </div>
        <div>
            --- Title (conditional -> Story) ---
        </div>
        <div>
            --- Cover Art (conditional -> Story) ---
        </div>
        <div id="optional_stuff" v-if="false">

            <div>
                --- Synopsis --- (conditional -> first chapter)
            </div>
            <div>
                --- Genres --- (conditional -> first chapter)
            </div>
            <div>
                --- Tags --- (conditional -> first chapter)
            </div>
            <div>
                --- Content Warnings --- (conditional -> first chapter)
            </div>
            
        </div>
        <div>
            --- Dropdown (conditional -> Story): Select Chapter ---
        </div>
        <div>
            --- Button (conditional -> Story): Create new Chapter ---
        </div>
        <div>
            --- Dropdown (conditional -> Story): Select World ---
        </div>
        <div>
            --- Small Button with popup: Create new World ---
        </div>
    </div>
    <div class="mx-2">
        <div class="control-section">
            <div class="sample-container">
                <div class="default-section">               
                    <ejs-richtexteditor id="default" ref="rteInstance" v-bind:value="value" ></ejs-richtexteditor>
                </div>
            </div>
        </div>
    </div>
    <div class="text-white">
        <div>
            --- Explanations? (Review process before submission?) ---
        </div>
        <div>
            --- Button: Submit Chapter ---
        </div>
    </div>
    </template>

<script setup>
import { RichTextEditorComponent as EjsRichtexteditor,Toolbar,Link,Image,HtmlEditor } from "@syncfusion/ej2-vue-richtexteditor"
import { provide, ref, onBeforeMount } from "vue"
import { useNavigationStore } from '@/store'

import DropDown from '@/components/DropDown.vue'
import axios from "axios"

const navigationStore = useNavigationStore()

onBeforeMount(() => {
    navigationStore.hideTopNav()
    navigationStore.hideResBars()
    navigationStore.storyDropDown = {
        'stories': {
            'd': ['test', 'Something something'],
            'placeholder': 'Select a story...',
            'showStoryDropdown': true
        }
    }
})

const rteInstance = ref(null)
const value = ref("<p>Some Text.</p>")
const richtexteditor =  [Toolbar, Link, Image, HtmlEditor]
provide('richtexteditor', richtexteditor)

async function loadStoryList () {
    axios.get()
}

</script>

<style>
@import "../../../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-lists/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../../../node_modules/@syncfusion/ej2-vue-richtexteditor/styles/material.css";
</style>
