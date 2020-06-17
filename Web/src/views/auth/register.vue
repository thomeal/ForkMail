<template>
  <el-dialog title="注册" width="40%" top="20vh" :show-close="false" :visible.sync="enabled" @closed="reset">
    <el-form :model="registration" :rules="rules" ref="login">
      <el-form-item label="手机号" :label-width="formLabelWidth" prop="username">
        <el-input v-model="registration.username"></el-input>
      </el-form-item>
      <el-form-item label="昵称" :label-width="formLabelWidth" prop="nickname">
        <el-input v-model="registration.nickname"></el-input>
      </el-form-item>
      <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
        <el-input v-model="registration.password"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="$emit('close')">取 消</el-button>
      <el-button type="primary" @click="register">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
  export default {
    name: "register",
    props: {
      visible: Boolean,
    },
    data() {
      return {
        rules: {
          username: [
            {validator: this.validateUsername, trigger: 'blur'}
          ],
          password: [
            {validator: this.validatePassword, trigger: 'blur'}
          ],
          nickname: [
            {validator: this.validateNickname, trigger: 'blur'}
          ]
        },
        formLabelWidth: '70px',
        registration: {
          username: '',
          nickname: '',
          password: ''
        }
      }
    },
    methods: {
      register() {
        this.$ref.register.validate(valid => {
          if (valid) {
            this.$axios({
              url: 'http://localhost:8000/register/',
              method: 'POST',
              data: {
                username: this.registration.username,
                password: this.registration.password,
                nickname: this.registration.nickname,
              }
            }).then(res => {
              if (res.data.success) {
                this.$message.success('注册成功');
                this.$emit('close');
              } else
                this.$message.error(res.data.error);
            }).catch(e => {
              this.$message.error('服务器开小差了');
            })
          }
        })
      },
      validateUsername(rule, value, callback) {
        let validateReg = /^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$/;
        if (validateReg.test(value))
          callback();
        else
          callback(new Error('请输入有效的手机号'))
      },
      validatePassword(rule, value, callback) {
        let validateReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/;
        if (validateReg.test(value))
          callback();
        else
          callback(new Error('8-16个字符，至少1个大写字母，1个小写字母和1个数字'))
      },
      validateNickname(rule, value, callback) {
        let validateReg = /^[\u4e00-\u9fff\w]{3,16}$/;
        if (validateReg.test(value))
          callback();
        else
          callback(new Error('3到16位字母,数字,汉字'))
      },
      reset() {
        Object.assign(this.$data, this.$options.data());
      }
    },
    computed: {
      enabled() {
        return this.visible;
      }
    },
  }
</script>

<style lang="scss" scoped>

</style>
