class CreateUsers < ActiveRecord::Migration[7.0]
  def change
    create_table :users do |t|
      t.string :account
      t.string :password_digest
      t.float :balance
      t.boolean :isVip

      t.timestamps
    end
  end
end
