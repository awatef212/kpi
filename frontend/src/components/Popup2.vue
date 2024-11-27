<template>
    <div v-if="isVisible" class="popup">
      <div class="popup-content">
        <slot></slot>
        <button @click="close">Fermer</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomPopup2',
    props: {
      isVisible: {
        type: Boolean,
        required: true
      }
    },
    methods: {
      close() {
        this.$emit('update:isVisible', false);
      }
    }
  };
  </script>
  
  <style>
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  }
  </style>
  