<template>
  <el-dialog id="userInfo" title="个人信息" :visible="visible" width="40%" @close="$emit('close')">
    <div class="accountInfo">
      <div class="strongTitle">
        账户信息
      </div>
      <div class="infoBlock">
        <div class="infoLine">
          <span class="infoBlack">昵称: </span>
          <span class="infoGray"> {{nickname}}</span>
        </div>
        <div class="infoLine">
          <span class="infoBlack">手机号: </span>
          <span class="infoGray"> {{mobile}}</span>
        </div>
      </div>
      <div class="strongTitle">
        邮箱信息
      </div>
      <div class="infoBlock">
        <div class="infoLine" v-for="(mail,index) in mails" :key="index">
          <span class="infoBlack">{{mail}}</span>
          <!--          <i class="el-icon-edit"/>-->
          <i class="el-icon-delete" @click="deleteMailBox(mail,index)"/>
        </div>
        <div class="infoLine">
          <i class="el-icon-plus" @click="addingMail=true"> 添加邮箱</i>
        </div>
      </div>
    </div>
    <el-dialog append-to-body title="添加邮箱" :visible="addingMail" width="40%">
      <el-form :model="newMail" :rules="rules" ref="newMail">
        <el-form-item label="地址" label-position="top" prop="address">
          <el-input v-model="newMail.address" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密钥" label-position="top" prop="key">
          <el-input v-model="newMail.key" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="IMAP服务器" label-position="top" prop="imapHost">
          <el-input v-model="newMail.imapHost" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="SMTP服务器" label-position="top" prop="smtpHost">
          <el-input v-model="newMail.smtpHost" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addingMail = false">取 消</el-button>
        <el-button type="primary" @click="addMail">确 定</el-button>
      </div>
    </el-dialog>
  </el-dialog>
</template>

<script>
  export default {
    name: "userInfo",
    props: {
      enabled: Boolean,
      mails: Array
    },
    data() {
      return {
        mobile: '',
        nickname: '',
        addingMail: false,
        newMail: {
          address: '',
          key: '',
          imapHost: '',
          smtpHost: ''
        },
        rules: {
          address: [
            {validator: this.validateAddress, trigger: 'blur'}
          ],
          key: [
            {required: true, message: '请输入密钥', trigger: 'blur'}
          ],
          imapHost: [
            {required: true, message: '请输入IMAP服务器地址', trigger: 'blur'}
          ],
          smtpHost: [
            {required: true, message: '请输入SMTP服务器地址', trigger: 'blur'}
          ]
        },
      }
    },
    methods: {
      addMail() {
        this.$refs.newMail.validate(valid => {
          if (valid) {
            this.$axios({
              url: 'http://localhost:8000/addMailBox/',
              method: 'POST',
              data: {
                token: localStorage['token'],
                email: this.newMail.address,
                key: this.newMail.key,
                smtpHost: this.newMail.smtpHost,
                imapHost: this.newMail.imapHost
              }
            }).then(res => {
              if (res.data.success) {
                this.addingMail = false;
                this.$message.success(res.data.message)
                this.$emit('add',this.newMail.address);
              } else
                this.$message.error(res.data.message)
            }).catch(e => {
              this.$message.error('服务器开小差了')
            })
          }
        })
      },
      deleteMailBox(mail,index) {
        this.$confirm('将删除该邮箱, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$axios({
            url: 'http://localhost:8000/deleteMailBox/',
            method: 'POST',
            data: {
              token: localStorage['token'],
              email: '\'' + mail + '\''
            }
          }).then(res => {
            if (res.data.success) {
              this.$message.success(res.data.message)
              this.$emit('delete',index);
            }
            else{
              this.$message.error(res.data.message)
            }
          }).catch(e=>{
            this.$message.error('服务器开小差了')
          })

        })
      },
      validateAddress(rule, value, callback) {
        let validateReg = new RegExp(/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/);
        if (validateReg.test(value))
          callback();
        else
          callback(new Error('请输入有效的邮箱地址'));
      }
    },
    computed: {
      visible() {
        return this.enabled;
      }
    },
    beforeMount() {
      this.nickname = localStorage['nickname'];
      this.mobile = localStorage['mobile'];
    }
  }
</script>

<style lang="scss">
  #userInfo {
    .el-dialog__body {
      padding: 0;
    }
  }
</style>

<style lang="scss" scoped>
  .el-form-item {
    margin-bottom: 10px;
  }

  .accountInfo {
    max-height: 500px;
    padding: 0 20px 10px;
    overflow: hidden;
    border: {
      top: rgba(214, 214, 214, 1.000) 1px solid;
      bottom: rgba(214, 214, 214, 1.000) 1px solid;
    }

    .strongTitle {
      margin-top: 10px;
      color: rgba(39, 62, 82, 1.000);
      font-weight: bold;
    }

    .infoBlack {
      color: rgba(39, 62, 82, 1.000);
    }

    .infoGray {
      color: rgba(128, 128, 128, 1.000);
    }

    .infoBlock {
      display: block;
      min-height: 50px;
      max-height: 200px;
      overflow: scroll;
      border: {
        top: rgba(214, 214, 214, 1.000) 1px solid;
        bottom: rgba(214, 214, 214, 1.000) 1px solid;
      }

      .infoLine {
        display: block;
        margin: 5px 5px;

        .el-icon-plus {

          &:hover {
            color: rgba(2, 122, 255, 1.000);
          }
        }

        .el-icon-edit {
          margin: 0 5px;

          &:hover {
            color: rgba(2, 122, 255, 1.000);
          }
        }

        .el-icon-delete {
          margin: 0 5px;

          &:hover {
            color: #d21b1b;
          }
        }
      }
    }
  }

</style>
