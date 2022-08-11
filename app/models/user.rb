# account:string
# password_digest:string
# balance:float
# isVip:boolean
#
# password:string virtual
# password_confirmation:string virtual
class User < ApplicationRecord
    has_secure_password

    #apenas permite contas com 5 dígitos e senhas com 4
    validates :account, presence: true, format: { with: /\b\d{5}\b/, message: "must have exactly 5 digits" }
    validates :password, presence: true, format: { with: /\b\d{4}\b/, message: "must have exactly 4 digits" }
end
