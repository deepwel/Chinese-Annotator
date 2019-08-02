<template>
  <div class="action-button">
      <ElButton class="button" @click="onClick">
        <i class="shortcuts-icon" :class="icon"></i>
        {{ name }}
      </ElButton>
  </div>
</template>

<script>
export default {
  name: 'action-button',
  props: {
    name: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: ''
    }
  },
  methods: {
    onClick: function() {
      this.$emit('onClick')
    }
  }
}
</script>

<style lang="scss" scoped>
.action-button {
  position: relative;
  width: 180px;
  height: 140px;
  display: inline-block;
}
</style>
