from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


LANGUAGE_CODES = {
    "hindi": "hin_Deva",
    "punjabi": "pan_Guru"
}


def translate_text(text: str, target_language: str = "hindi") -> str:

    lang_code = LANGUAGE_CODES.get(target_language.lower(), "hin_Deva")

    # encode input
    inputs = tokenizer(text, return_tensors="pt")

    # get token id safely
    target_lang_id = tokenizer.convert_tokens_to_ids(lang_code)

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=target_lang_id,
        max_length=200
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text