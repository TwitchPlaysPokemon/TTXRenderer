from typing import List


def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = []
    indent = "" if text.startswith("*") else ""
    subsequent_indent = "  " if text.startswith("*") else ""

    for word in words:
        # Check if adding the next word would exceed the width
        if sum(len(w) for w in current_line) + len(current_line) + len(word) + len(indent) > width:
            lines.append(indent + " ".join(current_line))
            current_line = [word]  # Start new line
            indent = subsequent_indent  # Use subsequent indent for next lines
        else:
            current_line.append(word)

    if current_line:  # Add any remaining words
        lines.append(indent + " ".join(current_line))

    return "\n".join(lines)


def process(
        page_number: int,
        position_in_set: int,
        size_of_set: int,
        position_in_section: int,
        size_of_section: int,
        section_title: str,
        paragraphs: List[str],
    ):
    line_count = 0
    yield b''.ljust(40)
    yield (b'\x177#4   k      \x07' + f"({position_in_set}/{size_of_set})".encode("utf-8")).ljust(40)
    yield b'\x17=l!5 5jh#i(s3                          '
    yield b'\x175 5ep5j*ss(p:                          '
    yield b'                                        '
    yield f'\x0d{section_title}\x0c({position_in_section}/{size_of_section})'.encode("utf-8").ljust(40)
    yield b''.ljust(40)
    yield b''.ljust(40)
    line_count += 8
    for p in paragraphs:
        lines = wrap_text(p.strip(), 39).split("\n")
        for line in lines:
            line = " " + line
            # Check for non-ASCII characters.
            if any(ord(c) > 127 for c in line):
                raise ValueError("Non-ASCII character in rule: " + line)

            yield line.encode("utf-8").ljust(40)
            line_count += 1
        yield b"".ljust(40)
        line_count += 1
    
    if position_in_set < size_of_set:
        yield f"\x03]P{page_number+1}".ljust(40).encode("utf-8")
    else:
        yield b" END".ljust(40)
    line_count += 1

    while line_count < 25:
        yield b"".ljust(40)
        line_count += 1


def render(
        page_number: int,
        position_in_set: int,
        size_of_set: int,
        position_in_section: int,
        size_of_section: int,
        section_title: str,
        paragraphs_str: str,
) -> List[bytes]:
    result = list(
        process(
            page_number,
            position_in_set,
            size_of_set,
            position_in_section,
            size_of_section,
            section_title,
            paragraphs_str
                .strip()
                .replace('“', '"')
                .replace('”', '"')
                .replace('’', "'")
                .split("\n\n"),
        ),
    )
    #if result[24] != b"":
    #    raise ValueError("Last line must be blank")
    return result 


def preamble_p1(page_number):
    position_in_set = 1 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 1
    section_title = "Preamble"
    s = """
        The aim of these rules is to           
        keep Twitch Plays Pokemon an enjoyable 
        place for everyone. We rewrote them    
        from the previous rules to make them   
        more like guidelines than laws, and to 
        make the more technical parts easier to
        enforce.                               

        It should be assumed that moderators   
        will use their own discretion towards  
        the more subjective guidelines, but    
        (respectfully) user feedback is always 
        welcome.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def scope_p1(page_number: int):
    position_in_set = 2 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 3
    section_title = "Scope"
    s = """
    The rules apply to the Twitch Plays Pokemon
    stream chat and any content displayed on stream,
    such as items, profile pictures and any
    in-game content (e.g. Pokemon nicknames).

    We have no jurisdiction over whispers, or
    peripherals such as Discord DMs, but in
    extreme cases we may issue bans over these
    things if we believe the person does not
    belong in our community.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def scope_p2(page_number: int):
    section_title = "Scope"
    position_in_set = 3 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 3
    s = """
    Be aware that these rules are in force community-wide, not just in stream. If you receive a timeout or ban from a community site, such as the community Discord or Subreddit, it may also result in a timeout or ban from the stream if the stream moderators determine your conduct also violates stream rules.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def scope_p3(page_number: int):
    section_title = "Scope"
    position_in_set = 4 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 3
    s = """
    These rules do not override the Twitch Community Guidelines, or any other official Twitch terms and guidelines, and we may issue punishments to enforce said guidelines.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p1(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 5 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 7
    s = """
        * Don't spam. Avoid flooding chat with long,
        repetitive, or nonsensical messages, as well
        as excessive use of emotes, caps lock, and
        special Unicode characters. The bot will
        automatically enforce this for the most
        part, but manual timeouts can be issued
        as well.

        * * Don't advertise things without mod permission.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p2(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 6 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 7
    s = """
        * Respect other users, and the chat as a whole. 

        * * Don't bully, harass, gaslight or slander users.

        * * Don't start fights or provoke people. Even in
        situations where there are arguments over different
        objectives, or in cases where some players are just
        inputting suboptimally, all sides must remain nice
        and respectful towards each other.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p3(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 7 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 7
    s = """
        * * Don't be a bigot. This covers all discrimination, identity hate and bigoted slurs.

        * * Don't get us wrong, a bit of trash-talking is still OK on TPP. But we don't take kindly to unnecessary and excessive, or derogatory insults or taunting.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p4(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 8 + 1
    size_of_set = 37
    position_in_section = 4
    size_of_section = 7
    s = """
        * No NSFW content. This includes nudity and other inappropriate and graphic content. Don't link to it, don't set it as your profile picture, don't make Unicode art of it.

        * * No fake NSFW links; URLs that look inappropriate but are really harmless will still be deleted.

        * * Discussing adult topics is OK, but don't write anything graphic or exceedingly shocking.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p5(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 9 + 1
    size_of_set = 37
    position_in_section = 5
    size_of_section = 7
    s = """
        * This is an English chat. Keep discussions 
        in other languages to a minimum, because we 
        can't reliably moderate them.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p6(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 10 + 1
    size_of_set = 37
    position_in_section = 6
    size_of_section = 7
    s = """
        * Don't be a minimod. This includes threatening 
        users with reports/timeouts, calling people alts 
        because they're new, and sending excessive 
        and frivolous reports to moderators. Please 
        tell us in Twitch whispers or Discord DMs 
        about people breaking the rules. If possible,
        avoid sending reports via public channels. 
        There's no need to incite public drama by doing so.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def basic_guidelines_p7(page_number: int):
    section_title = "Basic guidelines"
    position_in_set = 11 + 1
    size_of_set = 37
    position_in_section = 7
    size_of_section = 7
    s = """
        * Mods have the final say on what breaks the rules. Don't ignore a mod when they tell you to stop something. Our intention is for TPP to remain a fun and safe environment for everyone and so we reserve the right to act in any situation even if it's not covered by these rules if the need arises.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p1(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 12 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 7
    s = """
        We want TPP to be a place where everyone can experiment and
        play their way. So for the most part, you can input however
        you'd like. If you want to PC, learn a move, jump the ledge
        once or twice, throw a PBR match, go ahead!

        Of course, there are some exceptions:
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p2(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 13 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 7
    s = """
        * Don't knowingly try to break, crash, or softlock the stream unless an admin or operator gives explicit permission. And don't encourage others to do it, either.

        * Don't erase game progress unless an admin or operator gives explicit permission.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p3(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 14 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 7
    s = """
        * Runs: (1/2)

        * * Don't stop new gameplay for an unreasonable amount of time.
        Intentionally stopping us from progressing, or at least
        doing something new, for a long amount of time will be
        punished if it's only one person or a small number of
        people doing it. Since every situation is unique, mods will
        use their discretion to determine appropriate timings and
        punishments for each case.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p4(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 15 + 1
    size_of_set = 37
    position_in_section = 4
    size_of_section = 7
    s = """
        * Runs: (2/2)

        * * Don't intentionally use slurs or other derogatory names
        in any text prompt such as Pokemon nicknames. These will be
        treated as if you said them in chat and the offending text
        will be deleted.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p5(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 16 + 1
    size_of_set = 37
    position_in_section = 5
    size_of_section = 7
    s = """
        * PBR

        * * Don't intentionally try to lose money ("throw") so often
        that the game is unfun and predictable. 
        
        * * Don't throw a specific person in order to harass them. 
        
        * * Don't throw in collusion with another player(s) to get
        them higher on the leaderboard. This is match fixing.
        
        * * Don't draw out the length of a match for no good reason. 

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p6(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 17 + 1
    size_of_set = 37
    position_in_section = 6
    size_of_section = 7
    s = """
        * PBR

        * * Our goal with PBR moderation is to prevent malicious inputs
        from making the game less enjoyable for other bettors, not to
        prevent people from learning and making mistakes. The
        perceived intent of the inputs is what will determine
        the punishments.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def inputting_rules_p7(page_number: int):
    section_title = "Inputting rules"
    position_in_set = 18 + 1
    size_of_set = 37
    position_in_section = 7
    size_of_section = 7
    s = """
        * PBR

        * * * Since we know each match is a match and they
        don't exist in a void, a mod will generally give a
        warning before any timeout is issued and will
        generally wait at least 1 match after the warning
        before giving a timeout. Exceptions may be made
        when deemed necessary by mod discretion due to
        severity or repetition.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def alternate_accounts_p1(page_number: int):
    section_title = "Alternate accounts"
    position_in_set = 19 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 4
    s = """
        TPP has a complicated past with how we treat one person using multiple accounts. It is difficult to effectively enforce this, though. So our current policy is we don't really mind if you use a 2nd account (“alt”), as long as it's in good faith. But we'd strongly prefer it if you told us first.

        * First and foremost, we reserve the right to ban any obvious, unregistered alt on sight, even if it's not doing anything wrong.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def alternate_accounts_p2(page_number: int):
    section_title = "Alternate accounts"
    position_in_set = 20 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 4
    s = """
        * To prevent this from happening, please message a moderator with the username of your desired alt. Note that the alt will still be considered unregistered until we tell you that it has been registered (it will be entered into a database so the bot can recognize it). We may deny your request if we believe it to be in bad faith or you’re requesting an unreasonable number of alts just for the sake of it.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def alternate_accounts_p3(page_number: int):
    section_title = "Alternate accounts"
    position_in_set = 21 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 4
    s = """
        * Use only one account at a time. If you wish to switch accounts, you must wait one hour after sending a message on one account before you will be allowed to use the other. (The bot automatically enforces this for registered alts.)

        * Only one account can receive rewards (random pinball drops and PBR leaderboard rewards) at a time. The bot automatically handles this rule for registered alts.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def alternate_accounts_p4(page_number: int):
    section_title = "Alternate accounts"
    position_in_set = 22 + 1
    size_of_set = 37
    position_in_section = 4
    size_of_section = 4
    s = """
        * Do not use an alt maliciously. This includes impersonating other users, evading punishments, or inputting maliciously in PBR or runs. Doing so may induce heavier punishments for your main account.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def botting_p1(page_number: int):
    section_title = "Botting"
    position_in_set = 23 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 2
    s = """
        Any automatic sending of bets, inputs, and chat messages is not allowed. That is to say, every message you send must have a manual trigger. If we discover you are running a bot, you will be banned.

        All bots (other than tppsimulator) are ineligible for badge drops and other rewards. If a bot has obtained such rewards before it was discovered, it will be liquidated.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def botting_p2(page_number: int):
    section_title = "Botting"
    position_in_set = 24 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 2
    s = """
        Bots that simply read chat without sending messages, as well as bots that only whisper commands which don’t affect runs or PBR (badge trading, token storms, etc.) are allowed. Bots that do send messages require approval from mods/admins. Note that any bot that sends inputs will not be approved. The only exception to this is tppsimulator.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def punishments_p1(page_number: int):
    section_title = "Punishments"
    position_in_set = 25 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 3
    s = """
        Moderators will give timeouts as needed to enforce these guidelines and keep TPP enjoyable. Timeout lengths are generally scaled to severity and persistence, but are completely case-by-case; we make no guarantee of consistency.

        While you are timed out you should not have access to the bot via whispers, but in case you do, don’t abuse Mail or other items or we may extend your timeout.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def punishments_p2(page_number: int):
    section_title = "Punishments"
    position_in_set = 26 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 3
    s = """
        Bans are given in exceptional cases. They are indefinite in length and must be manually appealed. Typical cases for a ban include:
        
        * Racism, NSFW content, death threats, doxxing, etc.

        * Advertising or excessive spam within the first few messages.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def punishments_p3(page_number: int):
    section_title = "Punishments"
    position_in_set = 27 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 3
    s = """
        * Poor behavior that persists even after very long timeouts.

        * Unregistered alts, especially when they are abused.

        * Botting.

        To appeal your ban, use Twitch’s built-in Unban Request which will be available after a cooldown period after your ban.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p1(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 28 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 7
    s = """
        A PBR match will be manually canceled and recorded as a draw if: (1/2)
        
        * The game freezes or softlocks and is unrecoverable
        
        * If a softlock occurs and the match does not automatically cancel, but the match is not one where inputs affect the match (such as Defiance or Metronome), then it will be replayed from the start instead.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p2(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 29 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 7
    s = """
        A PBR match will be manually canceled and recorded as a draw if: (2/2)
        
        * A glitch caused by TPP (and not one solely within the game itself) alters or had a significant chance to alter the outcome of the match
        
        * If throwing done by alts, or throwing done in violation of the “Inputting Rules” section, altered the outcome of the match
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p3(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 30 + 1
    size_of_set = 37
    position_in_section = 3
    size_of_section = 7
    s = """
        If the match was not canceled before it ended, but falls into the cases above, it will be retroactively reverted to a draw (and balances will be adjusted accordingly).
        
        If a match was canceled and recorded as a draw, but it is clear that one side was going to win, and it was impossible for them to lose with any inputs if the match had played out, then the match will be retroactively recorded as a win for that side (and balances will be adjusted accordingly).
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p4(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 31 + 1
    size_of_set = 37
    position_in_section = 4
    size_of_section = 7
    s = """
        If a match that should have been canceled was not canceled,
        and its result radically altered balances, and this unfairly
        obtained money is multiplied in the following matches to
        radically alter the leaderboard, then further balance
        adjustments may be made.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p5(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 32 + 1
    size_of_set = 37
    position_in_section = 5
    size_of_section = 7
    s = """
        Tokens will be refunded in the following cases: (1/2)

        * If the hourly token match was canceled less than 2 minutes after it started, then tokens will be refunded for its bid.
        
        * If a battle song was bid for a match and it was canceled less than 2 minutes after it started, then tokens will be refunded for the bid.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p6(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 33 + 1
    size_of_set = 37
    position_in_section = 6
    size_of_section = 7
    s = """
        Tokens will be refunded in the following cases: (2/2)

        * If any song is bid and fails to play at all, tokens will be refunded for the bid.
        
        * If Pinball chooses the wrong table and gives a x0 payout, any bets on that table will be refunded.
        
        * If Pinball has achieved a score high enough to receive a payout, but crashes or achieves a lower score due to a glitch, tokens will be issued for the higher score.

    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def cancellations_and_refunds_p7(page_number: int):
    section_title = "Cancellation and refunds"
    position_in_set = 34 + 1
    size_of_set = 37
    position_in_section = 7
    size_of_section = 7
    s = """
        No items will be refunded for accidental consumption.
        
        Channel points will be refunded if their reward fails to work.
        
        Please contact a mod or admin if you think you are entitled to a refund.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def liquidations_p1(page_number: int):
    section_title = "Liquidations"
    position_in_set = 35 + 1
    size_of_set = 37
    position_in_section = 1
    size_of_section = 2
    s = """
        Alts before registration and bots will have their tokens, badges and items redistributed to random chat members (“liquidated”) after they are discovered. Users can also request to have their accounts liquidated for any reason. Note that user-requested liquidations will not be performed on demand and will in most cases be deferred for a month or more to give the user an opportunity to change their minds.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def liquidations_p2(page_number: int):
    section_title = "Liquidations"
    position_in_set = 36 + 1
    size_of_set = 37
    position_in_section = 2
    size_of_section = 2
    s = """
        Except as stated above we do not liquidate real users, even if they are inactive or banned.
    """
    return render(page_number, position_in_set, size_of_set, position_in_section, size_of_section, section_title, s)


def main():
    pages = [
        (800 + 1, preamble_p1(800 + 1)),
        (801 + 1, scope_p1(801 + 1)),
        (802 + 1, scope_p2(802 + 1)),
        (803 + 1, scope_p3(803 + 1)),
        (804 + 1, basic_guidelines_p1(804 + 1)),
        (805 + 1, basic_guidelines_p2(805 + 1)),
        (806 + 1, basic_guidelines_p3(806 + 1)),
        (807 + 1, basic_guidelines_p4(807 + 1)),
        (808 + 1, basic_guidelines_p5(808 + 1)),
        (809 + 1, basic_guidelines_p6(809 + 1)),
        (810 + 1, basic_guidelines_p7(810 + 1)),
        (811 + 1, inputting_rules_p1(811 + 1)),
        (812 + 1, inputting_rules_p2(812 + 1)),
        (813 + 1, inputting_rules_p3(813 + 1)),
        (814 + 1, inputting_rules_p4(814 + 1)),
        (815 + 1, inputting_rules_p5(815 + 1)),
        (816 + 1, inputting_rules_p6(816 + 1)),
        (817 + 1, inputting_rules_p7(817 + 1)),
        (818 + 1, alternate_accounts_p1(818 + 1)),
        (819 + 1, alternate_accounts_p2(819 + 1)),
        (820 + 1, alternate_accounts_p3(820 + 1)),
        (821 + 1, alternate_accounts_p4(821 + 1)),
        (822 + 1, botting_p1(822 + 1)),
        (823 + 1, botting_p2(823 + 1)),
        (824 + 1, punishments_p1(824 + 1)),
        (825 + 1, punishments_p2(825 + 1)),
        (826 + 1, punishments_p3(826 + 1)),
        (827 + 1, cancellations_and_refunds_p1(827 + 1)),
        (828 + 1, cancellations_and_refunds_p2(828 + 1)),
        (829 + 1, cancellations_and_refunds_p3(829 + 1)),
        (830 + 1, cancellations_and_refunds_p4(830 + 1)),
        (831 + 1, cancellations_and_refunds_p5(831 + 1)),
        (832 + 1, cancellations_and_refunds_p6(832 + 1)),
        (833 + 1, cancellations_and_refunds_p7(833 + 1)),
        (834 + 1, liquidations_p1(834 + 1)),
        (835 + 1, liquidations_p2(835 + 1)),
    ]
    for page_num, page in pages:
        with open(f"pages/P{page_num}-rules.txt", "wb") as f:
            for line in page:
                f.write(line + b"\n")


if __name__ == "__main__":
    main()
