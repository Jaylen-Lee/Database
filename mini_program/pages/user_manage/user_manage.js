// pages/passenger/passenger.js


Page({

  /**
   * 页面的初始数据
   */
  data: {
    user_list : [{
      account : "555555",username: "jksgjsbb",password : "6545646",noOfOrder:30
    },{
      account : "54654555",username: "jtbhbbsbb",password : "65415146",noOfOrder:30
    }],
    inputShowed : false,
    inputVal : ""
  },
  inputCom: function (e) {
    this.setData({
      inputVal: e.detail.value
    })
    console.log(this.data.inputVal);
  },
  /**
   * 生命周期函数--监听页面加载
   */
  /*onLoad: function () {
    // 发起请求
    var that = this
    wx.request({
      url: 'http://localhost:8080/Passenger/findbyuser',
      method: 'POST',
      data: {
        account : wx.getStorageSync('user').account
      },
      success: function (res) {
        // 请求成功，处理响应数据
        var data = res.data;
        //console.log(data);
        wx.setStorageSync('passenger', data)
          that.setData({
            passengers: data,
          });
      },
      fail: function (error) {
        // 请求失败，处理错误信息
        console.error('请求失败:', error);
      }
    });
  },*/
  search: function (e) {
    var key = e.detail.value;
    var that = this;

    // 发送请求
    wx.request({
      url: 'http://localhost:8080/Ad/finduser',
      method: 'GET',
      data: {
        account : that.data.inputVal
      },
      success: function (res) {
        // 请求成功，处理响应数据
        that.setData({
          user_list : res.data
        })
      },
      fail: function (error) {
        // 请求失败，处理错误信息
        that.setData({
          user_list : []
        })
        console.error('请求失败:', error);
      }
    });
  },
  hideInput() {
    this.setData({
      inputVal: '',
      inputShowed : false,
      tempstations : this.data.stations
    });
  },
  clearInput() {
    this.setData({
      inputVal: '',
      tempstations : this.data.stations
    });
  },
  showInput() {
    this.setData({
      inputShowed: true,
    });
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow : function () {
  },
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})