// pages/ticket/ticket.js

var util = require('../../utils/util.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    /*ticket_list: [{ticket_number:"00058002ad007a4137ad",train_number:"G107",depareture_station:"镇江南",destination_station:"苏州北",	fare:7511,	date:"2020-12-31",	id_number:"115392411616262566",	order_number:"652c66a58803090",	depareture_time:"12:43:00",	arrival_time:"13:21:00"},{ticket_number:"00058002ad007a4137ad",train_number:"G107",depareture_station:"lalala",destination_station:"苏州北",	fare:7511,	date:"2020-12-31",	id_number:"115392411616262566",	order_number:"652c66a58803090",	depareture_time:"12:43:00",	arrival_time:"13:21:00"}],*/
    ticket_list : [],
    status:"unpaid",
    // go_time: '',
    // arrive_time: '',
    name: '',
    order_number:"",

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var self = this;
    wx.request({
      url: 'http://localhost:8080/Ticket/findbyId',
      method: 'POST',
      data: {
        order_number: wx.getStorageSync('order_number')
      },
      success: function(res) {
        console.log(res.data)
        self.setData({
          ticket_list: res.data,
          name: wx.getStorageSync('user').name,
          order_number: wx.getStorageSync('order_number'),
          status: wx.getStorageSync('status')
        })
      }
    })
  },
  formSubmit1: function(e) {
        var self = this
        wx.request({
          url: 'http://localhost:8080/Order/refund',
          method: 'POST',
          data: {
            order_number:self.data.order_number
          },
          success: function(res) {
            self.setData({
                status: "refund",
            })
            if(res.data){
              wx.showToast({
                title: '退款成功',
                icon: 'success',
                duration: 2000
              })
            }
            else{
              wx.showToast({
                title: '退款失败',
                icon: 'error',
                duration: 2000
              })
            }
          }
        })
  },

  formSubmit2: function(e) {
        var self = this
        wx.request({
          url: 'http://localhost:8080/Order/completed',
          method: 'POST',
          data: {
            order_number: self.data.order_number
          },
          success: function(res) {
            self.setData({
              status:"completed"
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