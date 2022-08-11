class WithdrawsController < ApplicationController
    before_action :require_user_logged_in!
    def edit
    end

    def update
        if Current.user.update(balance_params)
            redirect_to balance_path, notice: "Balance updated!"
        else
            render :edit
        end
    end

    private
    
    def balance_params
        params.require(:user).permit(:balance)
    end
end