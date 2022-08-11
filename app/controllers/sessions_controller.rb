class SessionsController < ApplicationController
    def new
    end

    #valida cadastro do usuário para fazer login da sua conta
    def create
        user = User.find_by(account: params[:account])
        if user.present? && user.authenticate(params[:password])
            session[:user_id] = user.id
            redirect_to balance_path, notice: "Logged in successfully"
        else
            flash[:alert] = 'Invalid account or password'
            render :new
        end
    end

    #retira a conta do usuário como usuário logado atualmente
    def destroy
        session[:user_id] = nil
        redirect_to root_path, notice: "Logged out"
    end
end