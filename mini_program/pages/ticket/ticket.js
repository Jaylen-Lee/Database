// pages/ticket/ticket.js

var util = require('../../utils/util.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    ticket: {ticker_number:"00058002ad007a4137ad",train_number:"G107",depareture_station:"镇江南",destination_station:"苏州北",	fare:7511,	date:"2020-12-31",	id_number:"115392411616262566",	order_number:"652c66a58803090",	depareture_time:"12:43:00",	arrival_time:"13:21:00"},
    status:"unpaid"
    // go_time: '',
    // arrive_time: '',
    // name: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var self = this;
    wx.request({
      url: 'http://localhost:8080/ticket/findById',
      data: {
        ticket_id: wx.getStorageSync('ticket_id')
      },
      success: function(res) {
        self.setData({
          ticket: res.data,
          go_time: res.data.go_time.toString().substring(0, 5),
          arrive_time: util.formatTime(new Date(res.data.arrive_time)).split(' ')[1].substring(0, 5),
          name: wx.getStorageSync('user').name
        })
      }
    })
  },

  dishonour: function(e) {
    wx.request({
      url: 'http://localhost:8080/orders/delete',
      data: {
        order_number: wx.getStorageSync('order_number')
      }
    })
    wx.showToast({
      title: '退票成功',
      icon:'success',
      duration:1000
    })
    setTimeout(function () {
      wx.navigateBack({
      })
    }, 1000)
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