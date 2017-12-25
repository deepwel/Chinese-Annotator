<template>
  <div class="annotator">
    <div class="annotator-main">
      <el-card class="box-card">
        {{ sentence.content }}
      </el-card>
      <key-board-settings
        :annotations="annotations"
        @update="updateAnnotation"
        @onBlur="setKeyBoard"
      ></key-board-settings>
    </div>
    <div class="button-group">
      <div class="annotator-button-group">
        <tag
          v-for="annotation in annotations"
          :key="annotation.id"
          :size="tagSize"
          :name="annotation.name"
          :shortcuts="annotation.key"
          :selected="sentence.annotation_id === annotation.id"
          :machine-selected="sentence.machine_annotation_id === annotation.id"
          @selectTag="selectTag(annotation.id)"
        ></tag>
      </div>
      <div class="action-button-group">
        <action-button name="上一个(左键)" icon="el-icon-caret-left" @onClick="prev"></action-button>
        <action-button name="忽略(空格键)" icon="el-icon-close" @onClick="neglect"></action-button>
        <action-button name="下一个(右键)" icon="el-icon-caret-right" @onClick="next"></action-button>
      </div>
    </div>
  </div>
</template>

<script>
  import Tag from '../Tag'
  import Button from '../Button'
  import KeyBoardSettings from '../KeyBoardSettings'
  import mockData from '../../../mock'

  export default {
    name: 'text-classification',
    data: function () {
      return {
        sentence: null,
        sentences: [],
        annotations: []
      }
    },
    components: {
      'tag': Tag,
      'action-button': Button,
      'key-board-settings': KeyBoardSettings
    },
    computed: {
      tagSize: function () {
        return this.annotations.length > 5 ? 'small' : 'large'
      }
    },
    methods: {
      selectTag: function (selectedId) {
        this.sentence.annotation_id = selectedId
      },
      setKeyBoard: function () {
        let _this = this
        let annotationKeyBoard = {}

        for (const annotation of this.annotations) {
          if (annotation['keyCode']) {
            annotationKeyBoard[annotation['keyCode']] = annotation.id
          }
        }

        document.onkeydown = function () {
          let key = window.event.keyCode

          switch (key) {
            case 37:
              _this.prev()
              break
            case 39:
              _this.next()
              break
            case 32:
              _this.neglect()
              break
            default:
              const id = annotationKeyBoard[key]

              if (id) {
                _this.sentence.annotation_id = id
              }

              break
          }
        }
      },
      updateAnnotation: function (index, annotation) {
        this.annotations.map((tempAnnotation, idx) => {
          if (annotation.keyCode === tempAnnotation.keyCode) {
            this.annotations.splice(idx, 1, {
              id: tempAnnotation.id,
              name: tempAnnotation.name
            })
          }
        })

        this.annotations.splice(index, 1, annotation)
      },
      prev: function () {
        this.updateProgress()

        if (!this.sentence || this.sentence.id < 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id - 1]
      },
      neglect: function () {
        this.sentence.annotation_id = false
        this.updateProgress()

        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      },
      next: function () {
        this.updateProgress()

        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      },
      updateProgress: function () {
        if (this.sentences.length > 0) {
          let done = 0

          for (let sentence of this.sentences) {
            if (sentence.annotation_id !== null) {
              done++
            }
          }

          this.$store.commit('updateProgress', {
            done: done,
            count: this.sentences.length
          })
        }
      }
    },
    created: function () {
      new Promise((resolve, reject) => {
        const sentences = mockData.data.sentences

        for (const sentence of sentences) {
          if (!sentence.annotation_id) {
            this.sentence = sentence
            break
          }
        }

        this.sentences = sentences
        this.annotations = mockData.data.annotations
        this.$store.commit('updateBasic', mockData.data.basic)
        this.updateProgress()
        this.setKeyBoard()
      }).catch(err => {
        console.log(err)
      })
    }
  }
</script>

<style>
  .annotator{
    height: 100vh;
    display: flex;
    flex-direction: column;
    flex: 1;
    cursor: pointer;
    background: white;
    color: #333;
  }

  .annotator .annotator-main {
    flex: 1;
    display: flex;
    margin: 20px 20px 0 20px;
  }

  .annotator .box-card {
    flex: 1;
    margin-right: 20px;
    font-size: 24px;
    text-align: left;
    overflow-y: auto;
  }

  .annotator .button-group {
    width: 100%;
  }

  .annotator .button-group > div {
    width: 100%;
    display: flex;
    padding: 20px;
  }

  .annotator .button-group .annotator-button-group {
    justify-content: space-around;
  }

  .annotator .button-group .action-button-group {
    padding-top: 0;
    justify-content: space-between;
  }
</style>
