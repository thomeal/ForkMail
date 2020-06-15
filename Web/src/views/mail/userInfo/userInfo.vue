<template>
  <el-dialog :visible="visible" width="40%" @close="$emit('close')">

  </el-dialog>
</template>

<script>
  export default {
    name: "userInfo",
    props: {
      enabled: Boolean
    },
    data(){
      return{

      }
    },
    methods:{

    },
    computed:{
      visible(){
        return this.enabled;
      }
    }
  }
</script>

<style scoped>

</style>
