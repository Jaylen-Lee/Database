// pages/start/start.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    inputShowed: false,
    inputVal: '',
    stations:['北京','天津','上海'],
    tempstations : ['北京','天津','上海']
  },
  onInput: function(e) {
    const keyword = e.detail.value.trim();
    this.setData({
      inputVal: keyword
    });
    // 调用一个函数进行模糊匹配并更新页面展示
    this.filterStationList(keyword);
  },

  filterStationList: function(keyword) {
    // 根据关键字进行模糊匹配
    const filteredList = this.data.stations.filter(station => station.includes(keyword));
    // 更新页面展示
    this.setData({
      tempstations: filteredList
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var self=this;
    wx.request({
      url: 'http://localhost:8080/Station/findall',
      success:function(res){
        self.setData({
          stations: res.data,
          tempstations  :res.data
        })
      }
    })
  },

  bindSelect:function(e){
    wx.setStorageSync('startName', e.target.dataset.name)
    wx.switchTab({
      url: '../index/index'
    })

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