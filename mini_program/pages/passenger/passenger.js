// pages/passenger/passenger.js


Page({

  /**
   * 页面的初始数据
   */
  data: {
    passengers: [
      { name: '张三', id_number: '111111111111111111', phone: '18632495173', identity: false },
      { name: '李四', id_number: '563215321478541206', phone: '18236542973', identity: true },
      // 添加其他乘客信息
    ],
  },
  gotoAdd_passenger: function(e) {
      wx.navigateTo({
        url: '../add_passenger/add_passenger',
      })
  },
  editPassenger: function (event) {
    var passenger = event.currentTarget.dataset.passenger;

    // 将乘客信息存入缓存
    wx.setStorageSync('current_passenger', passenger);

    // 使用navigator组件跳转到修改界面
    wx.navigateTo({
      url: '/pages/modify_passenger/modify_passenger'
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
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