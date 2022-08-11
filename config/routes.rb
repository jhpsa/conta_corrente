# define a conexão entre os controllers e as views

Rails.application.routes.draw do
  get "balance", to: "balance#index"

  get "statement", to: "statements#index"

  get "withdraw", to: "withdraws#edit", as: :edit_withdraw
  patch "withdraw", to: "withdraws#update"

  get "deposit", to: "deposits#edit", as: :edit_deposit
  patch "deposit", to: "deposits#update"

  get "transference", to: "transferences#edit", as: :edit_transference
  patch "transference", to: "transferences#update"

  get "manager", to: "manager#index"

  get "password", to: "passwords#edit", as: :edit_password
  patch "password", to: "passwords#update"
  
  get "sign_up", to: "registrations#new"
  post "sign_up", to: "registrations#create"

  get "sign_in", to: "sessions#new"
  post "sign_in", to: "sessions#create"

  delete "logout", to: "sessions#destroy"

  root to: "main#index"
end