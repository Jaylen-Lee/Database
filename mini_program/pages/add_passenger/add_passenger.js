// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    name: '',
    id_number: '',
    phone: '',
    identity: '',
    typeList: ['成人', '学生'],
    index: '',
    hidden: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  formSubmit: function(e) {
    if (this.data.id_number && this.data.name && this.data.phone  && this.data.identity) {
        var self = this
        wx.request({
          url: 'http://localhost:8080/Passenger/add',
          data: {
            account : wx.getStorageSync('user').account,
            id_number: self.data.id_number,
            name: self.data.name,
            phone: self.data.phone,
            identity: self.data.identity == "学生" ? true : false
          },
          success: function(res) {
            self.setData({
              name: '',
              id_number: '',
              phone: '',
              identity: '',
              hidden:false
            })
            if(res.data){
              wx.showToast({
                title: '添加成功',
                icon: 'success',
                duration: 2000
              })
            }
            else{
              wx.showToast({
                title: '已经存在该乘客',
                icon: 'error',
                duration: 2000
              })
            }
          }
        })
      }
    else {
      wx.showModal({
        title: '温馨提醒',
        content: '请输入完整信息',
        showCancel: false
      })
    }
  },

  inputName: function(e) {
    this.setData({
      name: e.detail.value
    })
  },

  inputId: function(e) {
    this.setData({
      id_number: e.detail.value
    })
  },

  inputTel: function(e) {
    this.setData({
      phone: e.detail.value
    })
  },


  bindPickerChange: function(e) {
    this.setData({
      identity: this.data.typeList[e.detail.value],
      index: e.detail.value,
      hidden: true
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
