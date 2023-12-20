// pages/mycenter/mycenter.js


Page({
  data: {
    imageURL: '../../images/touxiang.png',
    hidden: true,
    account: '',
    password: '',
    user: {},
    flag: false, //用于标识用户是否登录
    is_ad : false  //标识是否为管理员账号
  },

  onLoad: function(options) {
    this.setData({
      flag: wx.getStorageSync('flag'),
    })
    //本地已经缓存了用户的登录状态，从后端返回数据
    if (wx.getStorageSync('flag')) {
      var self = this
      wx.request({
        url: 'http://localhost:8080//User/findby_account',
        data: {
          is_ad : wx.getStorageSync('is_ad'),
          account: wx.getStorageSync('user').account
        },
        success: function(res) {
          self.setData({
            user: res.data
          })
        }
      })
    }

  },
  // 显示登陆框
  login: function(e) {
    this.setData({
      hidden: false
    })
  },

  //登录验证
  formSubmit: function(e) {
    var self = this

    //console.log(wx.getStorageSync('match'))
    if (wx.getStorageSync('match')) {   //账号有效时，检查密码匹配与否
      this.setData({
        hidden: true
      })
      wx.request({
        url: 'http://localhost:8080//User/findby_account',
        data: {
          is_ad : self.data.is_ad,
          account: self.data.account
        },
        success: function(res) {
          // 密码匹配时，用户信息存到本地
          if (self.data.password == res.data.password) {
            self.setData({
              user: res.data,
              flag: true
            })
            wx.setStorageSync('user', res.data)
            wx.setStorageSync('flag', true)
            if (self.data.is_ad){
              wx.setStorageSync('is_ad', true)
            }
          }else{    //密码匹配错误
            wx.showToast({
              title: '密码错误',
              icon: 'none',
              duration: 1000
            })
          }
        },
      })
    } else {    //账号不存在
      wx.showToast({
        title: '账号不存在',
        icon: 'none',
        duration: 1000
      })
    }

  },
  //用户输入账号，并且已经离开输入框
  idInput: function(e) {
    var self = this
    wx.request({
      url: 'http://localhost:8080//User/findall_account',
      complete: function(res) {
        self.setData({
          account: e.detail.value
        })
        for (var i = 0; i < res.data.length; i++) {
          if (self.data.account == res.data[i]) {
            wx.setStorageSync('match', true)  //如果输入的账号有效，match=true
            break
          }
        }
      }
    })
  },
  // 输入密码，赋值给passward
  passwordInput: function(e) {
    this.setData({
      password: e.detail.value
    })
  },
  is_ad_change: function(e) {
    this.setData({
      is_ad: e.detail.value
    })
    // console.log(this.data.is_ad)
  },
  gotoOrders: function() {
    if (wx.getStorageSync('flag')) {
      wx.navigateTo({
        url: '../orders/orders',
      })
    } else {
      wx.showModal({
        title: '温馨提醒',
        content: '请先登录账户',
        showCancel: false
      })
    }
  },

  gotoUserInfo: function(e) {
    wx.navigateTo({
      url: '../userInfo/userInfo',
    })
  },

  gotoPassenger: function(e) {
    if (wx.getStorageSync('flag')) {
      wx.navigateTo({
        url: '../passenger/passenger',
      })
    } else {
      wx.showModal({
        title: '温馨提醒',
        content: '请先登录账户',
        showCancel: false
      })
    }
  },

  gotoModify: function(e) {
    if (wx.getStorageSync('flag')) {
      wx.navigateTo({
        url: '../modify_user/modify_user',
      })
    } else {
      wx.showModal({
        title: '温馨提醒',
        content: '请先登录账户',
        showCancel: false
      })
    }
  },
  // 取消时，隐藏登录界面
  cancel: function(e) {
    this.setData({
      hidden: true
    })
  },

  onShow: function() {
    this.onLoad()
  }
})