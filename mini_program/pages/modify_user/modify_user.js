// pages/modify/modify.js

Page({

  /**
   * 页面的初始数据
   */
  data: {
    user: { username : 'test',
    name: 'test',
    phone: 'test',},
    is_ad : false,
    username : '',
    name: '',
    phone: '',
    password: '',
    password_confirm: '',
    flag1: false,  //username
    flag2: false,   //name
    flag3: false,   //phone
    flag4: false,   //passward
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var self = this
    wx.request({
      url: 'http://localhost:8080/User/findby_account',
      data: {
        id: wx.getStorageSync('user').account
      },
      success: function(res) {
        self.setData({
          user: res.data,
          is_ad : wx.getStorageSync('is_ad')
        })
      }
    })

  },

  formSubmit: function(e) {
    var self = this;
  
    // 检查用户名是否为空字符串
    if (self.data.flag1 && !self.data.username.trim()) {
      // 如果用户名为空，则将flag1置为false，表示不修改用户名
      self.setData({
        flag1: false
      });
    }
  
    // 检查姓名是否为空字符串
    if (self.data.flag2 && !self.data.name.trim()) {
      // 如果姓名为空，则将flag2置为false，表示不修改姓名
      self.setData({
        flag2: false
      });
    }
  
    // 检查电话是否为空字符串
    if (self.data.flag3 && !self.data.phone.trim()) {
      // 如果电话为空，则将flag3置为false，表示不修改电话
      self.setData({
        flag3: false
      });
    }
  
    // 如果密码不为空且不匹配，则显示提示并返回
    if (this.data.password !== this.data.password_confirm) {
      wx.showModal({
        title: '温馨提醒',
        content: '密码输入不匹配，请重新输入',
        showCancel: false
      });
      return;
    }
  
    // 构建要发送到服务器的数据对象
    var userData = {
      id: wx.getStorageSync('user').account,
      username: (self.data.flag1 ? self.data.username.trim() : wx.getStorageSync('user').username),
      password: (self.data.password ? self.data.password : wx.getStorageSync('user').password)
    };
  
    // 如果是管理员，添加其他字段
    if (self.data.is_ad) {
      userData.name = (self.data.flag2 ? self.data.name.trim() : wx.getStorageSync('user').name);
      userData.phone = (self.data.flag3 ? self.data.phone.trim() : wx.getStorageSync('user').phone);
    }
    userData.id_ad = self.data.is_ad ? true : false;
    // console.log(userData)
    // 发送请求到服务器
    wx.request({
      url: 'http://localhost:8080/User/modify',
      data: userData,
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded' // Set the content type to form data
      },
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
  
  
  
  
  modifyusername: function(e) {
    this.setData({
      username: e.detail.value,
      flag1: true
    })
  },

  modifyname: function(e) {
    this.setData({
      name: e.detail.value,
      flag2: true
    })
  },

  modifyphone: function(e) {
    this.setData({
      phone: e.detail.value,
      flag3: true
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
