<?php
/* Template Name: Quiz Insolvency */

get_header();

// TODO: David remove inline css...
?>
<style>
	.slider--30perc {
		box-sizing: border-box;
		min-height: 126px;
	}

	@media (max-width: 991px) {

		.slider--30perc {
			min-height: 103px;
		}
	}

	.slider--alone {
		min-height: 94px;
	}

	@media (max-width: 991px) {

		.slider--alone {
			min-height:71px;
		}
	}
</style>
<main id="primary" class="site-main">
<div class="container">
	<div class="page-title-container">
		<h1 class="page-title"><?php the_title(); ?></h1>
	</div>
	<div class="quiz-page-content"><?php the_content();?></div>
	<div class="quiz-content">
		<div class="quiz-tab-container">
			<ul class="quiz-nav quiz-nav-tabs" id="quizTab-2" role="tablist">
				<li class="nav-item nav-item-1  active">
					<a class="nav-link" data-toggle="tab" role="tab">1. Situation</a>
				</li>
				<li class="nav-item nav-item-2 ">
					<a class="nav-link" data-toggle="tab" role="tab">2. Details</a>
				</li>
				<li class="nav-item nav-item-3 ">
					<a class="nav-link" data-toggle="tab" role="tab">3. Results</a>
				</li>
			</ul>
			<div class="quiz-tab-content">
				<div class=" quiz-tab-pane quiz-tab-1  active" id="quiz-tab-1" role="tabpanel">
					<div class="quiz-tab-content-inner">
						<div class="heading">How much does your company owe?</div>
						<p style="padding-top:10px">Use the sliders to define the amount of your debt</p>
						<div class="sliders">
							<div class="slider slider--30perc">
								<label for="quiz-amount-bank" class="quiz-amount-heading">Bank</label>
								<div class="slider-range-noUI-container">
									<div id="slider-range-bank" class="slider-range-noUI"></div>
								</div>
								<span class="quiz-amount quiz-amount-bank" id="quiz-amount-bank">£0</span>
							</div>
							<div class="slider  slider--30perc">
								<label for="quiz-amount-hmrc" class="quiz-amount-heading">HMRC</label>
								<div class="slider-range-noUI-container">
									<div id="slider-range-hmrc" class="slider-range-noUI"></div>
								</div>
								<span class="quiz-amount quiz-amount-hmrc" id="quiz-amount-hmrc">£0</span>
							</div>
							<div class="slider  slider--30perc">
								<label for="quiz-amount-creditors" class="quiz-amount-heading">Creditors</label>
								<div class="slider-range-noUI-container">
									<div id="slider-range-creditors" class="slider-range-noUI"></div>
								</div>
								<span class="quiz-amount quiz-amount-creditors" id="quiz-amount-creditors">£0</span>
							</div>
						</div>
					</div>
					<div class="quiz-tab-content-inner">
						<div class="heading">Does your limited company have any assets?</div>
						<p style="padding-top:10px">List the Approximate Value of Your Business Assets</p>
						<div class="slider slider-alone">
							<div id="slider-range-assets" class="slider-range"></div>
							<span class="quiz-amount quiz-amount-assets" id="quiz-amount-assets">£0</span>
						</div>
					</div>
					<div class="quiz-tab-content-inner  quiz-tab-content-inner-flex">
						<div class="quiz-tab-heading-container">
							<div class="heading">Do you have a personal guarantee?</div>
							<p style="padding-top:10px">Have you signed a personal guarantee document for your
								business?</p>
						</div>
						<div class="quiz-yes-no">
							<div class="quiz-radio-container active">
								<input type="radio" id="quiz-no" class="quiz-radio" name="guarantee" value="no"
									   checked>
								<label for="quiz-no">NO</label>
							</div>

							<div class="quiz-radio-container ">
								<input type="radio" id="quiz-yes" class="quiz-radio" name="guarantee" value="yes">
								<label for="quiz-yes">YES</label>
							</div>
						</div>
					</div>
					<div class="quiz-button-container">
						<button type="submit" href="#quiz-tab-2" class="quiz-button" data-value="0">Continue
						</button>
					</div>
				</div>
				<div class="quiz-tab-pane quiz-tab-2" id="quiz-tab-2" role="tabpanel">
					<div class="form-container">
						<div class="form-group">
							<?php echo do_shortcode( '[gravityform name="Insolvency Calculator" title="false" ajax="true"]' ); ?>
						</div>
						<div class="form-sidebar">
							<h4>Our Stressed Director's Guide explains:</h4>
							<ul class="form-sidebar-checklist">
								<li class="form-sidebar-item">What are the Implications of Insolvency for
									Directors?
								</li>
								<li class="form-sidebar-item">Your Company's Health Risk</li>
								<li class="form-sidebar-item">What Strategies are Available?</li>
								<li class="form-sidebar-item">What's the Liquidation Process?</li>
								<li class="form-sidebar-item">Role of the Insolvency Practitioner</li>
								<li class="form-sidebar-item">Dealing with HMRC Pressure</li>
							</ul>
							<div style="display: flex; justify-content: center; margin-bottom: 20px">
								<img width="150" height="183"
									 src="<?php echo CD_THEME_URL . 'assets/images/guide-220.png'; ?>"
									 alt="guidebook"
									 class="form-sidebar-image">
							</div>
						</div>
					</div>
				</div>
				</form>
			</div>
		</div>
	</div>
</div>
</main>

<?php
get_footer(); ?>

