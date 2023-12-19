// pages/modify/modify.js

Page({

  /**
   * 页面的初始数据
   */
  data: {
    passenger : {},
    name: '',
    phone: '',
    identity : false,
    flag1: false,
    flag2: false,
    flag3: false,

    typeList: ['成人', '学生'],
    index: '',
    hidden: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    // console.log(wx.getStorageSync('current_passenger'))
    this.setData({
      passenger : wx.getStorageSync('current_passenger')
    })
    wx.removeStorageSync('current_passenger')
    //console.log(wx.getStorageSync('current_passenger'))
    //console.log(wx.getStorageInfoSync())
  },

  formSubmit: function(e) {

    var self = this;
  
 
    if (self.data.flag1 && !self.data.name.trim()) {
      self.setData({
        flag1: false
      });
    }
  
    if (self.data.flag3 && !self.data.phone.trim()) {
      self.setData({
        flag3: false
      });
    }
    var data = {
      account: wx.getStorageSync('user').account,
      name: (self.data.flag1 ? self.data.name : self.data.passenger.name),
      identity: (self.data.flag2 ? self.data.identity :self.data.passenger.identity),
      phone: (self.data.flag3 ? self.data.phone :self.data.passenger.phone), 
      id_number: self.data.passenger.id_number, // Include the id_number parameter
    }
    // console.log(data) 
    wx.request({
      url: 'http://localhost:8080/Passenger/modify',
      data: data,
      method: 'POST',
      success: function(res) {
        wx.showToast({
          title: '修改成功',
          icon: 'success',
          duration: 1000
        });
  
        // 成功后返回上一页
        setTimeout(function() {
          wx.navigateBack({});
        }, 1000);
      },
      fail: function(err) {
        console.error('修改失败', err);
        // 处理请求失败的情况
      }
    });
  },
  delete : function(e){
    var self = this
    var data = {
      account: wx.getStorageSync('user').account,
      id_number : self.data.passenger.id_number
    }
    // console.log(data)
    wx.request({
      url: 'http://localhost:8080/Passenger/delete',
      data: data,
      success: function(res) {
        wx.showToast({
          title: '删除成功',
          icon: 'success',
          duration: 1000
        });
  
        // 成功后返回上一页
        setTimeout(function() {
          wx.navigateBack({});
        }, 1000);
      },
      fail: function(err) {
        console.error('删除失败', err);
        // 处理请求失败的情况
      }
    });
  },
  modifyname: function(e) {
    this.setData({
      name: e.detail.value,
      flag1: true
    })
  },

  bindPickerChange: function(e) {
    this.setData({
      identity : this.data.typeList[e.detail.value] == "学生" ? true : false,
      index: e.detail.value,
      flag2: true,
      hidden: true
    })
  },

  modifyphone: function(e) {
    this.setData({
      telphone: e.detail.value,
      flag3: true
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
