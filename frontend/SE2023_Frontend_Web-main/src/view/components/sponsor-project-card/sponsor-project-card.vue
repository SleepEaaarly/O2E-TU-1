<template>
  <a :href="['/sponsor_project/home/'+id]">
    <Card>
      <p class='title'>{{title}}</p>
      <p style="text-align: right;color:black">
        <span>赞助商：</span>
        <span class='sponsor'>{{sponsor}}</span>
        <p class='overview'>{{overview.substr(0,100)+'...'}}</p>
        <timeline :schedule=timeline style="margin-left: 15px;"></timeline>
    </Card>
  </a>
</template>
<script>
import timeline from '../timeline/timeline.vue'
export default {
  components: {
    timeline
  },
  props: {
    id: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: '太阳升起问题'
    },
    sponsor: {
      type: String,
      default: '剑门关桥东大学'
    },
    overview: {
      type: String,
      default: '行星运动问题引起了学者的广泛关注，我们赖以生存的太阳是如何运动的，一直吸引着人们去探索'
    },
    timeline: {
      type: Array,
      default: () => {
        return [
          { time: new Date(2020, 4, 1), event: '项目起始' },
          { time: new Date(2020, 4, 20), event: '第一次线上讨论会' },
          { time: new Date(2020, 5, 20), event: '第二次线上讨论会' },
          { time: new Date(2020, 6, 1), event: '项目结束' }
        ]
      }
    }
  },
  data () {
    return {

    }
  }
}

</script>

<style>
.title {
  text-align: left;
  box-sizing: border-box;
  overflow: hidden;
  margin: 0;
  display: block;
  font-size: 1.5rem;
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
  font-weight: 400;
  line-height: 1.33;
  letter-spacing: 0em;
  margin-bottom: 0.35em;
  color: black;
}
.sponsor {
  color: #1e88e5;
  font-size: 20px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.01071em;
  margin-bottom: 1em;
}
timeline {
  margin-left: 20px;
}

.overview {
  color: black;
}
</style>
