// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    account: '',  //用户账号
    password: '',   //密码
    password_confirm: '',   //确认密码
    user_name:'',   //用户名
    hidden: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  formSubmit: function(e) {
    //console.log(this.data)
    // console.log(wx.getStorageSync('day'))
    if (this.data.account && this.data.user_name && this.data.password && this.data.password_confirm) {
      if (this.data.password != this.data.password_confirm) {
        wx.showModal({
          title: '温馨提醒',
          content: '密码输入不匹配，请重新输入',
          showCancel: false
        })
      } else {
        var self = this
        wx.request({
          url: 'http://localhost:8080/User/register',
          data: {
            account: self.data.account,
            username: self.data.user_name,
            password: self.data.password
          },
          success: function(res) {
            self.setData({
              user_name: '',
              account: '',
              password:'',
              password_confirm:'',
              hidden:false
            })
            wx.showToast({
              title: '注册成功',
              icon: 'success',
              duration: 2000
            })
          }
        })
        /*wx.showToast({
          title: '注册成功',
          icon: 'success',
          duration: 2000
        })*/
      }
    } else {
      wx.showModal({
        title: '温馨提醒',
        content: '请输入完整信息',
        showCancel: false
      })
    }
  },

  inputAccount: function(e) {
    this.setData({
      account : e.detail.value
    })
  },

  inputUser_name: function(e) {
    this.setData({
      user_name: e.detail.value
    })
  },

  

  inputPassword: function(e) {
    this.setData({
      password: e.detail.value
    })
  },

  inputPasswordConfirm: function(e) {
    this.setData({
      password_confirm: e.detail.value
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})