<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">ForkMail</div>
      <el-form :model="authInfo" :rules="rules" ref="login" label-width="0px" class="ms-content">
        <el-form-item prop="username">
          <el-input v-model="authInfo.username" placeholder="请输入手机号" @keyup.enter.native="login()">
            <el-button slot="prepend" icon="el-icon-user"/>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="请输入密码"
            v-model="authInfo.password"
            show-password
            @keyup.enter.native="login()">
            <el-button slot="prepend" icon="el-icon-lock"/>
          </el-input>
        </el-form-item>
        <div class="btn">
          <el-button type="primary" @click="login()">登录</el-button>
        </div>
        <div class="btn">
          <el-button type="success" @click="registering=true">注册</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
  import Register from "./register";

  export default {
    components: {Register},
    data: function () {
      return {
        registering: false,
        authInfo: {
          username: '',
          password: '',
        },
        rules: {
          username: [{required: true, message: '请输入手机号', trigger: 'blur'}],
          password: [{required: true, message: '请输入密码', trigger: 'blur'}],
        }
      };
    },
    methods: {
      login() {
        this.$refs.login.validate((valid) => {
          if (valid) {
            this.$axios({
              url: 'http://localhost:8000/login',
              method: 'GET',
              params: {
                username: this.authInfo.username,
                password: this.authInfo.password
              },
            }).then(res => {
              if (res.data.success) {
                this.$message.success(res.data.message);
                localStorage['token'] = res.data.token;
                this.$router.push('mail');
              } else this.$message.error(res.data.message);
            }).catch(error => {
                this.$message.error("服务器开小差了");
              });
          } else {
            this.$message.error('请输入用户名密码');
          }
        });
      },
    },
  };
</script>

<style scoped>
  .login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background-size: 100%;
    background: url(" ../../assets/1.jpg") no-repeat center;
    background-size: cover;
  }

  .ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #fff;
    border-bottom: 1px solid #ddd;
    font-family: "Bitstream Vera Sans Mono", Monaco, "Courier New", Courier, monospace;
  }

  .ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(150, 161, 170, 0.6);
    overflow: hidden;
  }

  .ms-content {
    padding: 30px 30px;
    text-align: center;
  }

  .btn {
    text-align: center;
  }

  .btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
  }
</style>
