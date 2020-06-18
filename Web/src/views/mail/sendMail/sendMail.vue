<template>
  <el-dialog :show-close="false" id="userInfo" title="发送邮件" :visible="visible" width="40%" @close="$emit('close')">
    <div class="accountInfo">
      <div class="infoBlock">
        <el-form :model="header" :rules="rules" ref="mail">
          <div class="infoLine">
            <el-form-item prop="receiver">
              <el-input
                placeholder="收件人"
                prefix-icon="el-icon-user"
                v-model="header.receiver">
              </el-input>
            </el-form-item>
          </div>
          <div class="infoLine">
            <el-form-item prop="subject">
              <el-input
                placeholder="主题"
                prefix-icon="el-icon-date"
                v-model="header.subject">
              </el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>
      <div class="infoBlock" style="border: none">
        <el-input
          type="textarea"
          :rows="5"
          resize="none"
          placeholder="邮件内容"
          v-model="content">
        </el-input>
      </div>
      <div class="footer">
        <el-button @click="$emit('close')">取 消</el-button>
        <el-button type="primary" @click="sendMail">确 定</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
  export default {
    name: "sendMail",
    props: {
      enabled: Boolean,
      reply: String,
      mail: String
    },
    data() {
      return {
        header: {
          receiver: '',
          subject: '',
        },
        content: '',
        rules: {
          receiver: [
            {validator: this.validateReceiver, trigger: 'blur'}
          ],
          subject: [
            {validator: this.validateSubject, trigger: 'blur'}
          ]
        },
      }
    },
    methods: {
      validateReceiver(rule, value, callback) {
        let validateReg = new RegExp(/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/);
        if (validateReg.test(value))
          callback();
        else
          callback(new Error('请输入有效的邮箱地址'));
      },
      validateSubject(rule, value, callback) {
        if (!value)
          callback(new Error('请输入邮件主题'));
        else
          callback();
      },
      sendMail(){
        this.$refs.mail.validate(valid=>{
          if (valid){
            this.$axios({
              url: 'http://localhost:8000/sendMail/',
              method: 'POST',
              data:{
                mail: '\''+this.mail+'\'',
                receiver: this.header.receiver,
                subject: this.header.subject,
                content: this.content,
                token: localStorage['token']
              }
            }).then(res=>{
              if (res.data.success) {
                this.$emit('close');
                this.$message.success(res.data.message);
              }
              else
                this.$message.error(res.data.message);
            }).catch(e=>{
              this.$message.error('服务器开小差了');
            })
          }
        })
      }
    },
    computed: {
      visible() {
        return this.enabled;
      }
    },
    watch: {
      visible: {
        handler() {
          this.header.receiver = this.reply;
        },
        immediate: true,
        deep: true
      }
    }
  }
</script>

<style lang="scss" scoped>
  .accountInfo {
    max-height: 500px;
    padding: 0 20px 10px;
    overflow: hidden;
    position: relative;
    border: {
      top: rgba(214, 214, 214, 1.000) 1px solid;
      bottom: rgba(214, 214, 214, 1.000) 1px solid;
    }

    .infoBlock {
      padding: 10px 0;
      display: block;
      min-height: 50px;
      max-height: 200px;
      overflow: scroll;
      border: {
        bottom: rgba(214, 214, 214, 1.000) 1px solid;
      }

      .infoLine {
        display: block;
        margin: 5px 5px;

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

    .footer {
      float: right;
    }
  }
</style>
