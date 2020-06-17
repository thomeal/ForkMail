<template>
  <el-dialog :show-close="false" id="userInfo" title="个人信息" :visible="visible" width="40%" @close="$emit('close')">

  </el-dialog>
</template>

<script>
  export default {
    name: "sendMail",
    props: {
      enabled: Boolean,
      reply: String
    },
    data() {
      return {
        receiver: ''
      }
    },
    computed: {
      visible() {
        return this.enabled;
      }
    },
    beforeMount() {
      this.receiver = this.reply;
    }
  }
</script>

<style lang="scss" scoped>

</style>
