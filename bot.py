if user_id not in game_state["players"]: return
        val_str = query.data.split("_")[1]
        if val_str == "FREE": return
        val = int(val_str)
        
        if val in game_state["drawn"]:
            game_state["players"][user_id]["marked"].add(val)
            await query.edit_message_reply_markup(reply_markup=build_keyboard(user_id))
        else:
            await query.answer("❌ ይህ ቁጥር ገና አልወጣም!", show_alert=True)

    elif query.data == "check_bingo":
        if user_id not in game_state["players"] or not game_state["active"]: return
        player = game_state["players"][user_id]
        if check_win(player["card"], player["marked"]):
            game_state["active"] = False
            for pid in game_state["players"]:
                await context.bot.send_message(
                    chat_id=pid,
                    text=f"🏆 BINGO! አሸናፊው {player['name']} ነው!\n\nአዲስ ጨዋታ ለመጀመር /start ይጫኑ።",
                    parse_mode="Markdown"
                )
            game_state["players"].clear()
        else:
            await query.answer("❌ ገና አልዘጉም! 5 ቁጥሮችን በመስመር ይምቱ።", show_alert=True)

async def draw_numbers(context: ContextTypes.DEFAULT_TYPE):
    all_nums = list(range(1, 76))
    random.shuffle(all_nums)
    letters = ["B", "I", "N", "G", "O"]

    for pid in game_state["players"]:
        await context.bot.send_message(chat_id=pid, text="🚀 ጨዋታው ተጀምሯል! ቁጥሮች በየ 5 ሰከንዱ ይወጣሉ...")

    for num in all_nums:
        if not game_state["active"]:
            break
        await asyncio.sleep(5)
        if not game_state["active"]:
            break
            
        game_state["drawn"].append(num)
        letter = letters[(num - 1) // 15]
        
        for pid in list(game_state["players"].keys()):
            try:
                await context.bot.send_message(chat_id=pid, text=f"🎱 የወጣው ቁጥር፦ {letter}-{num}", parse_mode="Markdown")
            except Exception:
                pass

    if game_state["active"]:
        game_state["active"] = False
        game_state["players"].clear()

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("ቦቱ ስራ ጀምሯል...")
    app.run_polling()

if name == "main":
    main()
