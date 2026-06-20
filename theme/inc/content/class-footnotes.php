<?php

namespace CD\Content;

/**
 * Description
 *
 * @package CD\Content
 * @author  webpigment
 * @licence  GPL-2
 */

class Footnotes {
	private $content;
	private $count;
	private $footnotes;
	private $title;
	private $description;

	/**
	 * @param string $content . Finding footnotes marked with ((
	 */
	public function __construct( $content ) {
		$content = preg_replace( '/<script\b[^>]*>(.*?)<\/script>/is', '', $content );

		preg_match_all(
			'(\(\((.*?)\)\))',
			$content,
			$match
		);


		$this->content             = $content;
		$this->count               = count( $match );
		$this->footnotes['search'] = $match[0];
		$this->footnotes['text']   = $match[1];
		$this->title               = get_field( 'footnotes_title', 'option' );
		$this->description         = get_field( 'footnotes_description', 'option' );

		if ( ! $this->title ) {
			$this->title = 'References';
		}
	}

	/*
	 * Reducing found footnotes to unique ones with and without brackets included
	 */
	private function geUniqueFootnotes() {


		$this->footnotes['search'] = array_values( array_unique( $this->footnotes['search'] ) );
		$this->footnotes['text']   = array_values( array_unique( $this->footnotes['text'] ) );

		$this->count = count( $this->footnotes['search'] );
	}

	/*
	 * Dislaying references for footnotes
	 */
	private function AddReferencesForFootnotes() {

		$this->content .= '<section class="ep-footnotes__section">';
		$this->content .= '<div class="ep-footnotes__title">' . $this->title . '</div>';
		$this->content .= '<div class="ep-footnotes__description">' . $this->description . '</div>';

		$this->content .= '<ol class="ep-footnotes">';
		for ( $i = 0; $i < $this->count; $i ++ ) {
			$this->content .= '<li id="footnote__' . ( $i + 1 ) . '" class="ep-footnote__text">' . $this->footnotes['text'][ $i ] . '</li>';
		}

		$this->content .= '</ol>';
		$this->content .= '</section>';
	}

	/*
	 * Replacing footnote markup with <sup> number
	 * Adding HTML for internal linkage and tooltip
	 */
	private function MarkupContentWithFootnotes() {
		$img_src = CD_THEME_URL . '/assets/images/icon-footnote.png';
		for ( $i = 0; $i < $this->count; $i ++ ) {
			$footnote_nr   = $i + 1;
			$footnote_html = '<span class="ep-footnote__referrer">';
			$footnote_html .= '<a class="ep-footnote__referrer-link" href="#footnote__'.($i+1).'">';
			$footnote_html .= '<sup>['.($i+1).']</sup>';
			$footnote_html .= '</a>';
			$footnote_html .= '<span class="ep-footnote__tooltip-outer">';
			$footnote_html .= '<span class="ep-footnote__tooltip">' . $this->footnotes['text'][ $i ] . '</span>';
			$footnote_html .= '</span></span>';
			$this->content = str_replace(
				$this->footnotes['search'][ $i ],
				$footnote_html,
				$this->content
			);
		}

	}

	/**
	 * Get a modified post with a content marked up with footnotes and references.
	 *
	 * @return string
	 */
	public function getPostFootnotesMarkup() {
		$this->geUniqueFootnotes();
		if ( $this->count > 0 ) {
			$this->MarkupContentWithFootnotes();
			$this->AddReferencesForFootnotes();
		}

		return $this->content;
	}
}

