// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    passenger_List: [{
      "name": "李金霖",
      "id_number": "110110110110110110",
      "phone": "17773333888",
      "identity": 1,
      "tick":true,
    },{
      "name": "大春",
      "id_number": "222110110110110110",
      "phone": "16673333888",
      "identity": 0,
      "tick":true,
    }],
    identity_list:[],
    id_list: [],
    hidden: true,
    count: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  checkboxChange(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    const items = this.data.passenger_List
    const values = e.detail.value
    console.log(values.length)
    this.setData({
      count: values.length
    })
    this.setData({
      id_list: values
    })
    var v1 = [];
    for (let i = 0; i < values.length; i++) {
      for (let j = 0; j < items.length; j++) {
        if (items[j].id_number === values[i]) {
          v1.push(items[j].identity);
        }
      }
    }
    this.setData({
      identity_list: v1
    })
  },

  formSubmit: function (e) {
    if (!this.data.count) {
      var self = this
      wx.request({
        url: 'http://localhost:8080/Passenger/choose',
        data: {
          // 发送所有选中乘客id和身份数据
          account: wx.getStorageSync('user').account,
          count: self.data.count,
          id_list: self.data.id_list,
          identity_list: self.data.identity_list
        },
        success: function (res) {
          self.setData({
            hidden: false
          })
          if (res.data) {
            wx.showToast({
              title: '购票成功，请前往订单页面查询车票',
              icon: 'success',
              duration: 2000
            })
          } else {
            wx.showToast({
              title: '购票失败',
              icon: 'error',
              duration: 2000
            })
          }
        }
      })
    } else {
      wx.showModal({
        title: '温馨提醒',
        content: '请选择乘客！',
        showCancel: false
      })
    }
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