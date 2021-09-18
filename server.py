from waitress import serve
import admin
serve(admin.app, host='0.0.0.0', port=80)