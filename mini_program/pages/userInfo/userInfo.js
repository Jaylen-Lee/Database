// pages/userInfo/userInfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
      user : {},
    /*user:{
      account : "123567",
      username : "aad",
      name : "阿萨大大",
      password : "78946",
      phone : "763787268"
    },*/
    is_ad : false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var self=this
    wx.request({
      url: 'http://localhost:8080/User/findby_account',
      data:{
        account :wx.getStorageSync('user').account,
        is_ad : wx.getStorageSync('is_ad')
      },
      success:function(res){
        self.setData({
          user:res.data
        })
      }
    })
    
  },

  bindSelect:function(e){
    wx.clearStorageSync()
    /*wx.removeStorageSync('user')
    wx.removeStorageSync('ticket_id')
    wx.removeStorageSync('order_number')

    wx.setStorageSync('flag', false)
    wx.setStorageSync('match', false)*/

    wx.showToast({
      title: '退出成功',
      icon: 'success',
      duration: 1000
    })
    setTimeout(function(){
      wx.navigateBack({
      })
    },100)

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})