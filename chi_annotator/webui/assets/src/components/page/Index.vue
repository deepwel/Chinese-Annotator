<template>
  <div id="annotator-page" class="page">
    <menu-bar :basic="basic" :progress="progress"></menu-bar>
    <div class="annotator">
      <el-card class="box-card">
        {{ sentence.content }}
      </el-card>
      <div class="button-group">
        <div class="annotator-button-group">
          <tag
            v-for="annotation in annotations"
            :key="annotation.id"
            :name="annotation.name"
            :shortcuts="annotation.id + 1 + ''"
            :selected="sentence.annotation_id === annotation.id"
            :machine-selected="sentence.machine_annotation_id === annotation.id"
            @selectTag="selectTag(annotation.id)"
          ></tag>
        </div>
        <div class="action-button-group">
          <action-button name="上一个(左键)" icon="el-icon-caret-left" @onClick="prev"></action-button>
          <action-button name="忽略(X键)" icon="el-icon-close" @onClick="neglect"></action-button>
          <action-button name="下一个(右键)" icon="el-icon-caret-right" @onClick="next"></action-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import MenuBar from '../common/MenuBar'
  import Tag from '../common/Tag'
  import Button from '../common/Button'
  import mockData from '../../mock'

  export default {
    name: 'Loading',
    data: function () {
      return {
        sentence: null,
        sentences: [],
        annotations: [],
        basic: null
      }
    },
    components: {
      'menu-bar': MenuBar,
      'tag': Tag,
      'action-button': Button
    },
    computed: {
      progress: function () {
        if (this.sentences.length > 0) {
          let done = 0

          for (let sentence of this.sentences) {
            if (sentence.annotation_id !== null) {
              done++
            }
          }

          return {
            done: done,
            count: this.sentences.length
          }
        }

        return null
      }
    },
    methods: {
      selectTag: function (selectedId) {
        this.sentence.annotation_id = selectedId
      },
      prev: function () {
        if (!this.sentence || this.sentence.id < 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id - 1]
      },
      neglect: function () {
        this.sentences.annotation_id = false

        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      },
      next: function () {
        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      }
    },
    created: function () {
      new Promise((resolve, reject) => {
        const sentences = mockData.data.sentences
        let component = this

        for (const sentence of sentences) {
          if (!sentence.annotation_id) {
            this.sentence = sentence
            break
          }
        }

        this.sentences = sentences
        this.annotations = mockData.data.annotations
        this.basic = mockData.data.basic

        document.onkeydown = function () {
          let key = window.event.keyCode

          switch (key) {
            case 37:
              component.prev()
              break
            case 39:
              component.next()
              break
            case 88:
              component.next()
              break
            default:
              const number = key - 48

              if (number > 0 && number < component.annotations.length + 1) {
                component.sentence.annotation_id = number - 1
              }
              break
          }
        }
      }).catch(err => {
        console.log(err)
      })
    }
  }
</script>

<style>
  .page{
    width:100%;
    height:100%;
    display: flex;
  }

  .annotator{
    height: 100vh;
    display: flex;
    flex-direction: column;
    flex: 1;
    cursor: pointer;
    background: white;
    color: #333;
  }

  .annotator .box-card {
    margin: 20px;
    flex: 1;
    font-size: 24px;
    text-align: left;
  }

  .annotator .button-group {
    height: 400px;
    width: 100%;
  }

  .annotator .button-group > div {
    height: 200px;
    width: 100%;
    display: flex;
    padding: 20px;
  }

  .annotator .button-group .annotator-button-group {
    justify-content: space-around;
  }

  .annotator .button-group .action-button-group {
    justify-content: space-between;
  }
</style>
