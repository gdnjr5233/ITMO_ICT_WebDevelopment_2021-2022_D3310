<template>
  <v-data-table
    :headers="headers"
    :items="cells"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title>Cells</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog
          v-model="dialog"
          max-width="500px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="green"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              +
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.cell"
                      label="Cell"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.row"
                      label="Row"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.tsekh"
                      label="Tsekh"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue darken-4"
                text
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios'
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    flag: false,
    headers: [
      {
        text: 'Cells',
        align: 'start',
        sortable: false,
        value: 'name'
      },
      { text: 'Cell', value: 'cell' },
      { text: 'Row', value: 'row' },
      { text: 'Tsekh', value: 'tsekh' },
      { text: 'Actions', value: 'actions', sortable: false }
    ],
    cells: [],
    editedIndex: -1,
    editedItem: {
      cell: 0,
      row: 0,
      tsekh: 0
    },
    defaultItem: {
      cell: 0,
      row: 0,
      tsekh: 0
    }
  }),
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    }
  },
  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    }
  },
  created () {
    this.cellsList()
  },
  methods: {
    async cellsList () {
      try {
        const response = await this.axios
          .get('http://127.0.0.1:8000/poultry/cells/list')
        if (response.status !== 200) {
          throw new Error(response.status)
        }
        this.cells = response.data
        return response.data
      } catch (e) {
        console.error('AN API ERROR', e)
      }
    },
    editItem (item) {
      this.editedIndex = this.cells.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem (item) {
      this.editedIndex = this.cells.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },
    deleteItemConfirm () {
      if (this.editedIndex > -1) {
        this.cells.splice(this.editedIndex, 1)
        this.closeDelete()
        axios.delete('http://127.0.0.1:8000/poultry/cells/info/' + JSON.stringify(this.editedItem.id), {
          id: this.editedItem.id,
          cell: this.editedItem.cell,
          row: this.editedItem.row,
          tsekh: this.editedItem.tsekh
        })
      } else {
        this.cells.push(this.editedItem)
      }
      this.close()
    },
    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.cells[this.editedIndex], this.editedItem)
        axios.put('http://127.0.0.1:8000/poultry/cells/info/' + JSON.stringify(this.editedItem.id), {
          id: this.editedItem.id,
          cell: this.editedItem.cell,
          row: this.editedItem.row,
          tsekh: this.editedItem.tsekh
        })
          .then(response => {
            console.log(response)
            // ans = response.status
          })
          .catch(error => {
            console.log(error)
            console.log('posting new data . . .')
            // ans = error.status
            axios.post('http://127.0.0.1:8000/poultry/cells/create/', {
              cell: this.editedItem.cell,
              row: this.editedItem.row,
              tsekh: this.editedItem.tsekh
            })
          })
      }
      this.close()
    }
  }
}
</script>
