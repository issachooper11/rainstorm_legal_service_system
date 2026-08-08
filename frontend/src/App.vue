<template>
  <router-view />
</template>

<script setup>
// App.vue 作为根组件，只需负责渲染当前路由对应的页面
</script>

<style>
/* 清除默认边距，让后台管理占满全屏 */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background-color: #f5f7fa;
}
</style>