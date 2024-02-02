<template>
    <div class="fixed top-0 left-0 w-full h-full text-white flex items-center justify-center bg-black opacity-70 z-50">
      <div class="spinner-container">
        <div class="spinner"></div>
      </div>
    </div>
  </template>

<style scoped>
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.spinner {
  border: 8px solid #ffffff;
  border-top: 8px solid transparent;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
