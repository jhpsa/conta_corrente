class RegistrationsController < ApplicationController
    def new
        @user = User.new
    end

    #cria usuário normal sem saldo
    def create
        @user = User.new(user_params)
        @user.balance = 0
        @user.isVip = false
        if @user.save
            session[:user_id] = @user.id
            redirect_to balance_path, notice: "Successfully created account"
        else
            render :new
        end
    end

    private

    #permite que atributos do usuário sejam acessados
    def user_params
        params.require(:user).permit(:account, :password, :password_confirmation, :balance, :isVip)
    end
end