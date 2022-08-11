class ApplicationController < ActionController::Base
    before_action :set_current_user

    #define usuário logado atualmente
    def set_current_user
        if session[:user_id]
            Current.user = User.find_by(id: session[:user_id])
        end
    end

    #impede que usuários não logados acessem páginas que necessitam de login
    def require_user_logged_in!
        redirect_to sign_in_path, alert: "You must be signed in to do that." if Current.user.nil?
    end
end
