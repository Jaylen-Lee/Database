// pages/quary/quary.js
var util = require('../../utils/util.js');

Page({
  /**
   * 页面的初始数据
   */
  data: {
    ticketList: [{start_station : '上海',
    arrive_station : '北京西',
    go_time: 'hh:mm',
    arrive_time : 'hh:mm',
    train_number: 'E568',
    price : '333',
    go_date: 'yyyy-mm-dd',
    remain: '1199'}],
    start_station:'',
    arrive_station:'',
    go_date:'',
    hidden: false,
    hidden_2 : true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var self = this
    wx.request({
      url: 'http://localhost:8080/Train/query',
      data: {
        start_station: wx.getStorageSync('startName'),
        arrive_station: wx.getStorageSync('endName'),
        go_date: wx.getStorageSync('year') + '-' + wx.getStorageSync('month') + '-' + wx.getStorageSync('day'),
      },
      success: function(res) {
        console.log(res.data)
        if (res.data.length>0) {
          self.setData({
            hidden_2 : true,
            ticketList: res.data
          })
          console.log(self.data.ticketList)

        }
      }
    })

  },

  buyTicket: function(e) {
    wx.navigateTo({
      url: '../choose_passenger/choose_passenger',
    })
    // wx.setStorageSync('ticket_id', e.currentTarget.dataset.ticketId)
    wx.setStorageSync('go_date', e.currentTarget.dataset.goDate)
    wx.setStorageSync('train_number', e.currentTarget.dataset.trainNumber)
    wx.setStorageSync('go_time', e.currentTarget.dataset.gotime)
    wx.setStorageSync('arrive_time', e.currentTarget.dataset.arrivetime)
    wx.setStorageSync('start_station', e.currentTarget.dataset.startstation)
    wx.setStorageSync('arrive_station', e.currentTarget.dataset.arrivestation)
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
