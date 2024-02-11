<template>
    <div id="app">
      <div id='container' style="margin:50px auto 0; width:250px;">
          <br>
          <ejs-dropdownlist id='dropdownlist' :popupHeight="props.height" :popupWidth="props.width" 
          :dataSource='props.stories.d' :placeholder='props.placeholder'></ejs-dropdownlist>
      </div>
    </div>
</template>

<script setup>
import { DropDownListComponent as EjsDropdownlist } from "@syncfusion/ej2-vue-dropdowns";

const props = defineProps({
    stories: {
        type: Object,
        default: {
            'd': ['Test', 'test2']
        }
    },
    placeholder : {
        type: String,
        default: ''
    },
    height: {
        type: String,
        default: '200px'
    },
    width: {
        type: String,
        default: '250px'
    }
})

console.log(props.stories)
            
</script>

<style>
  @import "../../node_modules/@syncfusion/ej2-base/styles/material.css";
  @import "../../node_modules/@syncfusion/ej2-inputs/styles/material.css";
  @import "../../node_modules/@syncfusion/ej2-vue-dropdowns/styles/material.css";
</style>