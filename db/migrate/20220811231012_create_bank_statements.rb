class CreateBankStatements < ActiveRecord::Migration[7.0]
  def change
    create_table :bank_statements do |t|
      t.date :date
      t.time :time
      t.string :description
      t.float :value
      t.integer :account_id

      t.timestamps
    end
  end
end
