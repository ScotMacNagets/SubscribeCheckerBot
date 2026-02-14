#Main

class AdminMain:
    OPEN = "admin_open"

#Users

class AdminUsers:
    HUMAN_RESOURCE = "admin_human_resource"
    SEARCH_BY_USERNAME = "admin_users_search_id"
    USER_DETAIL_PREFIX = "admin_user_"  # admin_user_<user_id>


class AdminUserActions:
    EXTEND = "admin_user_extend"
    SET_END_DATE = "admin_user_set_end"
    CANCEL_SUB = "admin_user_cancel_sub"
    DELETE_USER = "admin_user_delete"
    BACK_TO_USERS_ADMIN_MENU = "admin_back_users_admin_menu"
    BACK_TO_ADMIN_MENU="admin_back_main"

#Tariff

class AdminTariffs:
    TARIFFS_MENU = "admin_tariffs_menu"
    BACK_TO_ADMIN_MENU = "admin_tariffs_back_main"
