<template>
  <div v-if="timeline.length>0">
    <Steps :current="current" direction="vertical">
      <Step v-for='(schedule_item,index) in timeline' :key='index' :title="formatDate(schedule_item.time)" :content='schedule_item.event'></Step>
    </Steps>
  </div>
</template>

<script>
export default {
  data () {
    return {

    }
  },
  props: {
    schedule: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  methods: {
    formatDate: function (date) {
      var y = date.getFullYear()
      var m = date.getMonth() + 1
      m = m < 10 ? ('0' + m) : m
      var d = date.getDate()
      d = d < 10 ? ('0' + d) : d
      var h = date.getHours()
      var minute = date.getMinutes()
      minute = minute < 10 ? ('0' + minute) : minute
      var second = date.getSeconds()
      second = minute < 10 ? ('0' + second) : second
      return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second
    }
  },
  computed: {
    timeline () {
      return this.schedule.map(x => ({
        event: x.event,
        time: new Date(x.time)
      }))
    },
    current: function () {
      return this.timeline.map(s => (s.time < Date.now() ? 1 : 0)).reduce((a, b) => (a + b))
    }
  }
}
</script>

<style>
</style>
